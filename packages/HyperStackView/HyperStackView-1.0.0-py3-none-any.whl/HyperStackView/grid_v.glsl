#version 330 core

attribute vec2 aPos;

varying vec2 vTexCoord;

uniform mat4 uM;

void main() {
	gl_Position = vec4(aPos, 0.0, 1.0) * mat4(
		2, 0, 0, -1,
		0, 2, 0, -1,
		0, 0, 0, -1,
		0, 0, 0, 1
    ) * uM;
    vTexCoord = aPos;
}
