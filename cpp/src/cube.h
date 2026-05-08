// Copyright (c) 2022 Pierre DEJOUE
// This code is distributed under the terms of the MIT License
#pragma once

#include <bitset>
#include <cstdint>
#include <ostream>
#include <vector>

namespace rubik {

/**
 * Abstraction of the 2x2x2 Rubiks' cube
 *
 * It is assumed that corner 7 (LUF) of the cube is fixed
 */
namespace two_by_two {

struct Cube
{
    // Corner 7 (LUF) is fixed and therefore not represented
    // Position of corners 0 to 6
    std::uint8_t permutation[7];
    // Orientation of corners 0 to 6
    std::uint8_t orientations[7];
};

// e.g. "01634527:00200010"
std::ostream& operator<<(std::ostream& out, const Cube& cube);

using CubeIndex = std::uint32_t;

constexpr std::uint32_t PERMUT_MASK = 0x03FFF000;
constexpr std::uint32_t ORIENT_MASK = 0x00000FFF;
constexpr std::uint32_t MAX_NB_CONFIGS = 1 << 26;
static_assert((PERMUT_MASK | ORIENT_MASK) == (MAX_NB_CONFIGS - 1));

using ConfigBitset = std::bitset<MAX_NB_CONFIGS>;

CubeIndex serialize(const Cube& cube);
Cube deserialize(CubeIndex idx);

const Cube& solved_cube();

using Rotation = Cube;

Cube apply_rotation(const Rotation& rot, const Cube& cube);

// With corner 7 (LUF) being fixed, the allowed rotations are R, D, B
const Rotation& Rot_R();
const Rotation& Rot_R2();
const Rotation& Rot_R3();   // R'

const Rotation& Rot_D();
const Rotation& Rot_D2();
const Rotation& Rot_D3();   // D'

const Rotation& Rot_B();
const Rotation& Rot_B2();
const Rotation& Rot_B3();   // B'

// All possible rotations assuming corner 7 is fixed
const std::vector<Rotation>& all_rotations();

} // namespace two_by_two
} // namespace rubik
