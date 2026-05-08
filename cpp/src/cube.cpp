// Copyright (c) 2022 Pierre DEJOUE
// This code is distributed under the terms of the MIT License
#include "cube.h"

#include <algorithm>
#include <bitset>
#include <cassert>
#include <cstdint>
#include <numeric>
#include <ostream>
#include <vector>

namespace rubik {
namespace two_by_two {

std::ostream& operator<<(std::ostream& out, const Cube& cube)
{
    std::size_t idx = 0;
    for (idx = 0; idx < 7; ++idx)
        out << (int)cube.permutation[idx];
    out << 7 << ':';
    for (idx = 0; idx < 7; ++idx)
        out << (int)cube.orientations[idx];
    out << 0;
    return out;
}

CubeIndex serialize(const Cube& cube)
{
    static bool used_perm[7];
    std::fill(&used_perm[0], &used_perm[7], false);

    const std::uint8_t* permut = cube.permutation;
    const std::uint8_t* orient = cube.orientations;

    // First 3 permutations are encoded as is
    std::uint32_t permutation = permut[0];
    permutation <<= 3;
    permutation |= permut[1];
    permutation <<= 3;
    permutation |= permut[2];
    used_perm[permut[0]] = used_perm[permut[1]] = used_perm[permut[2]] = true;

    // Next 2 permutations are encoded with 2 bits
    const auto encode_2bits = [&](std::size_t idx) {
        const auto encoded = std::count(&used_perm[0], &used_perm[permut[idx]], false);
        assert(encoded < 4);
        permutation |= encoded;
        used_perm[permut[idx]] = true;
    };
    permutation <<= 2;
    encode_2bits(3);
    permutation <<= 2;
    encode_2bits(4);

    // Next permutation is encoded with 1 bit
    permutation <<= 1;
    const auto encoded = std::count(&used_perm[0], &used_perm[permut[5]], false);
    assert(encoded < 2);
    permutation |= encoded;

    // Last permutation is implicit

    // Orientation are encoded with two bits each. The last one is implicit
    std::uint32_t orientation = 0u;
    for (std::size_t idx = 0u, shift = 0u; idx < 6; ++idx, shift += 2)
    {
        orientation |= (orient[idx] & 0x03) << shift;
    }

    return (PERMUT_MASK & (permutation << 12)) | (ORIENT_MASK & orientation);
}

Cube deserialize(CubeIndex idx)
{
    Cube cube;

    static bool used_perm[7];
    std::fill(&used_perm[0], &used_perm[7], false);

    const std::uint32_t permutation = (idx & PERMUT_MASK) >> 12;
    const std::uint32_t orientation = idx & ORIENT_MASK;

    const std::uint32_t perm_0 = (permutation & 0x00003800) >> 11;
    const std::uint32_t perm_1 = (permutation & 0x00000700) >> 8;
    const std::uint32_t perm_2 = (permutation & 0x000000E0) >> 5;
    const std::uint32_t perm_3 = (permutation & 0x00000018) >> 3;
    const std::uint32_t perm_4 = (permutation & 0x00000006) >> 1;
    const std::uint32_t perm_5 = (permutation & 0x00000001);

    cube.permutation[0] = perm_0;
    used_perm[perm_0] = true;
    cube.permutation[1] = perm_1;
    used_perm[perm_1] = true;
    cube.permutation[2] = perm_2;
    used_perm[perm_2] = true;

    const auto decode_perm = [&](std::uint32_t encoded) {
        std::size_t idx = 0u;
        for (idx = 0u; idx < 6; ++idx)
        {
            if (used_perm[idx])
                continue;
            if (encoded == 0)
                break;
            encoded--;
        }
        assert(encoded == 0);
        assert(!used_perm[idx]);
        used_perm[idx] = true;
        return idx;
    };

    cube.permutation[3] = decode_perm(perm_3);
    cube.permutation[4] = decode_perm(perm_4);
    cube.permutation[5] = decode_perm(perm_5);
    cube.permutation[6] = decode_perm(0);

    std::uint8_t sum_orientation = 0u;
    for (std::size_t idx = 0u, shift = 0u; idx < 6; ++idx, shift += 2)
    {
        cube.orientations[idx] = (orientation >> shift) & 0x03;
        sum_orientation += cube.orientations[idx];
    }
    cube.orientations[6] = (30 - sum_orientation) % 3;

    return cube;
}

const Cube& solved_cube()
{
    static const Cube cube = []() {
        Cube cube;
        std::iota(&cube.permutation[0], &cube.permutation[7], std::uint8_t{ 0 });
        std::fill(&cube.orientations[0], &cube.orientations[7], std::uint8_t{ 0 });
        return cube;
    }();
    return cube;
}

Cube apply_rotation(const Rotation& rot, const Cube& cube)
{
    Cube result;
    std::size_t idx = 0;
    for (idx = 0; idx < 7; ++idx)
       result.permutation[idx] = rot.permutation[cube.permutation[idx]];
    for (idx = 0; idx < 7; ++idx)
       result.orientations[idx] = (rot.orientations[cube.permutation[idx]] + cube.orientations[idx]) % 3;
    return result;
}

const Rotation& Rot_R() {
    static const Rotation Rot_R = Rotation {
        { 0, 5, 1, 3, 4, 6, 2 },
        { 0, 1, 2, 0, 0, 2, 1 }
    };
    return Rot_R;
}

const Rotation& Rot_R2()
{
    static const Rotation Rot_R2 = []() { return apply_rotation(Rot_R(), Rot_R()); }();
    return Rot_R2;
}

const Rotation& Rot_R3()
{
    static const Rotation Rot_R3 =  []() { return apply_rotation(Rot_R(), Rot_R2()); }();
    return Rot_R3;
}

const Rotation& Rot_D()
{
    static const Rotation Rot_D = Rotation {
        { 4, 0, 2, 3, 5, 1, 6 },
        { 0, 0, 0, 0, 0, 0 ,0 }
    };
    return Rot_D;
}

const Rotation& Rot_D2()
{
    static const Rotation Rot_D2 = []() { return apply_rotation(Rot_D(), Rot_D()); }();
    return Rot_D2;
}

const Rotation& Rot_D3()
{
    static const Rotation Rot_D3 =  []() { return apply_rotation(Rot_D(), Rot_D2()); }();
    return Rot_D3;
}

const Rotation& Rot_B()
{
    static const Rotation Rot_B = Rotation {
        { 1, 2, 3, 0, 4, 5, 6 },
        { 1, 2, 1, 2, 0, 0, 0 }
    };
    return Rot_B;
}

const Rotation& Rot_B2()
{
    static const Rotation Rot_B2 = []() { return apply_rotation(Rot_B(), Rot_B()); }();
    return Rot_B2;
}

const Rotation& Rot_B3()
{
    static const Rotation Rot_B3 =  []() { return apply_rotation(Rot_B(), Rot_B2()); }();
    return Rot_B3;
}

const std::vector<Rotation>& all_rotations() {
    static const std::vector<Rotation> ALL_ROTATIONS = {
        Rot_R(), Rot_R2(), Rot_R3(),
        Rot_D(), Rot_D2(), Rot_D3(),
        Rot_B(), Rot_B2(), Rot_B3(),
    };
    return ALL_ROTATIONS;
}

} // namespace two_by_two
} // namespace rubik
