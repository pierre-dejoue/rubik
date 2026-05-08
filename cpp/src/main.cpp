/*******************************************************************************
 *
 * Find the God's number of the 2x2x2 Rubik's cube.
 *
 * https://en.wikipedia.org/wiki/God%27s_algorithm
 *
 * Copyright (c) 2022 Pierre DEJOUE
 * This code is distributed under the terms of the MIT License
 *
 ******************************************************************************/
#include "cube.h"

#include <cassert>
#include <cstdlib>
#include <cstdint>
#include <iostream>
#include <memory>

std::size_t configurations_add_one_move(
    const rubik::two_by_two::ConfigBitset& prev_configs,
    rubik::two_by_two::ConfigBitset& new_configs,
    rubik::two_by_two::ConfigBitset& all_configs)
{
    constexpr auto MAX_NB_CONFIGS = rubik::two_by_two::MAX_NB_CONFIGS;

    assert(prev_configs.size() == MAX_NB_CONFIGS);
    assert(new_configs.size()  == MAX_NB_CONFIGS);
    assert(all_configs.size()  == MAX_NB_CONFIGS);

    new_configs.reset();
    std::size_t count_new_configs = 0u;
    for (std::size_t config_idx = 0u; config_idx < MAX_NB_CONFIGS; ++config_idx)
    {
        if (prev_configs.test(config_idx))
        {
            assert(all_configs.test(config_idx));
            const auto cube = rubik::two_by_two::deserialize(config_idx);
            for (const auto& rotation : rubik::two_by_two::all_rotations())
            {
                auto new_config_idx = serialize(apply_rotation(rotation, cube));
                if (!all_configs.test(new_config_idx))
                {
                    assert(!prev_configs.test(new_config_idx));
                    new_configs.set(new_config_idx);
                    all_configs.set(new_config_idx);
                    count_new_configs++;
                }
            }
        }
    }
    return count_new_configs;
}

std::uint8_t find_god_number()
{
    std::uint8_t god_nb = 0u;

    using ConfigBitset = rubik::two_by_two::ConfigBitset;
    auto configs_a = std::make_unique<ConfigBitset>();
    auto configs_b = std::make_unique<ConfigBitset>();
    auto all_configs = std::make_unique<ConfigBitset>();
    configs_a->reset();
    configs_b->reset();

    configs_a->set(rubik::two_by_two::serialize(rubik::two_by_two::solved_cube()));     // Initial configuration of the cube, the solved state
    *all_configs = *configs_a;

    ConfigBitset* prev_configs = configs_a.get();
    ConfigBitset* new_configs = configs_b.get();

    while (true)
    {
        const auto nb_new_configs = configurations_add_one_move(*prev_configs, *new_configs, *all_configs);
        if (nb_new_configs == 0)
            break;
        god_nb++;
        std::cout << std::dec << int(god_nb) << ": " << nb_new_configs << std::endl;
        std::swap(prev_configs, new_configs);
    }
    std::cout << "Reachable configurations: " << std::dec << all_configs->count() << std::endl;

    return god_nb;
}

int main(int argc, char *argv[])
{
    using Cube = rubik::two_by_two::Cube;
    const Cube solved_cube = rubik::two_by_two::solved_cube();
    std::cout << "Find the God's number of the 2x2x2 Rubik's cube" << std::endl;
    std::cout << solved_cube << std::endl;
    const auto solved_idx = rubik::two_by_two::serialize(solved_cube);
    std::cout << "0x0" << std::hex << solved_idx << std::endl << rubik::two_by_two::deserialize(solved_idx) << std::endl;
    const auto idx = 5625472;
    const auto cube = rubik::two_by_two::deserialize(idx);
    std::cout << "0x0" << std::hex << idx << std::endl << cube << std::endl << "0x0" << rubik::two_by_two::serialize(cube) << std::endl;
    const auto god_nb = find_god_number();
    std::cout << "God's number: " << std::dec << int(god_nb) << std::endl;
    return 0;
}
