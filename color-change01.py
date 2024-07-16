import re
import colorsys

def is_dark_color(hex_color):
    """判断颜色是否较暗"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    return l < 0.5

def lighten_color(hex_color, factor=0.2):
    """调高颜色亮度"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    l = min(1, l + factor)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    def replace_color(match):
        color = match.group(1)
        if is_dark_color(color):
            return f'"foreground": "{lighten_color(color)}"'
        return match.group(0)

    # 匹配 "foreground": "#RRGGBB" 格式的颜色
    pattern = re.compile(r'"foreground":\s*"(#(?:[0-9a-fA-F]{3}){1,2})"')
    new_content = pattern.sub(replace_color, content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

if __name__ == '__main__':
    process_file('themes/theme-dark.json')
