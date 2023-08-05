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

varying float vDiffuseComponent;
varying vec3 vPos;
varying vec2 vTexCoord;

uniform sampler2D tTex;

const vec3 LIGHT_DIFFUSE = vec3(.5, .7, .4);
const vec3 LIGHT_DIFFUSE_INSIDE = vec3(.7, .4, .4);
const vec3 LIGHT_AMBIENT = vec3(.1);
const float ALPHA = 1.0;

void main() {
	gl_FragColor = vec4(
		(gl_FrontFacing ? LIGHT_DIFFUSE : LIGHT_DIFFUSE_INSIDE) * vDiffuseComponent
			+ LIGHT_AMBIENT,
	ALPHA) * texture(tTex, vTexCoord);
}
