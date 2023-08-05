#version 330 core

varying vec2 vTexCoord;

uniform sampler2D tGrid;
uniform float uBrightness;

void main() {
    vec4 px_color = texture(tGrid, vec2(vTexCoord.xy));

    if (px_color.a < .1) discard;

    gl_FragColor = uBrightness * (
        gl_FrontFacing ?
            px_color
            : vec4(.5, .5, .8, 1.) * px_color
    );
}

