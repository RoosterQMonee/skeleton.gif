import base64

def to_c_array(path):
    with open(path, "rb") as f:
        data = f.read()

    out = []
    for i, b in enumerate(data):
        out.append(f"0x{b:02x}")

    return ", ".join(out), len(data)

atlas_data, atlas_size = to_c_array("assets/atlas.png")
meta_data, meta_size = to_c_array("assets/meta.json")
audio_data, audio_size = to_c_array("assets/riff.mp3")

header = f"""
#pragma once
#include <stddef.h>
#include <stdint.h>

static const unsigned char ATLAS_PNG[] = {{
{atlas_data}
}};

static const unsigned int ATLAS_PNG_SIZE = {atlas_size};

static const unsigned char META_JSON[] = {{
{meta_data}
}};

static const unsigned int META_JSON_SIZE = {meta_size};

static const unsigned char RIFF_MP3[] = {{
{audio_data}
}};

static const unsigned int RIFF_MP3_SIZE = {audio_size};
"""

with open("src/assets_embedded.h", "w") as f:
    f.write(header)

print("Embedded assets generated")