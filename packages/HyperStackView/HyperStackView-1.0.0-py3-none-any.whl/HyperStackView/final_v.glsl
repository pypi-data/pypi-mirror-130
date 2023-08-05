#version 330 core
/*
 * HyperStackView -- application for rendering 3D raster images
 * Copyright (C) 2021  Jiří Wolker
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

attribute vec2 aScreenCoord;

varying vec4 vTexCoord;

uniform float scale;

void main() {
	vTexCoord = vec4(aScreenCoord, 0.0, 1.0);
	gl_Position = vTexCoord * mat4(
		2.0 * scale, 0.0, 0.0, -1.0,
		0.0, 2.0 * scale, 0.0, -1.0,
		0.0, 0.0, 0.0, 0.0,
		0.0, 0.0, 0.0, 1.0
	);
}
