import math, urllib.request
from PIL import Image, ImageDraw

# urllib setup (precaution)
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

def get_user_avatar(avatar_url):
        file, _ = urllib.request.urlretrieve(avatar_url)
        return file

def create_bg():
    mode = 'RGB'
    size = (1000, 1000)
    color = '#2978b5'
    bg = Image.new(mode, size, color)
    print('created background')
    return bg

def create_mask(image):
    alpha = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([(0, 0), image.size], 0, 360, fill=255)
    return alpha

def create_image(center_avatar_url, layers_config):
    bg = create_bg()
    gap = 10
    bg_w, bg_h = bg.size
    center_avatar = Image.open(get_user_avatar(center_avatar_url)).convert('RGB')
    center_avatar = center_avatar.resize((160, 160))
    bg.paste(center_avatar, ((bg_w - 160)//2, (bg_h - 160)//2), create_mask(center_avatar))
    print('pasted central avatar')
    for layer in layers_config:
        image_count = layer['image_count']
        users = layer['users']
        gaps_count = image_count-1
        R = layer['radius']
        circuit = 2*math.pi*R
        diagonal = int((circuit - gaps_count*gap) / image_count)
        no_of_image = 0
        base_angle = 360/image_count
        for user in layer['users']:
            file, _ = urllib.request.urlretrieve(users[user]['avatar'])
            avatar = Image.open(file).convert('RGB')
            h = diagonal
            w = diagonal
            avatar = avatar.resize((h, w))
            angle_x = math.cos(math.radians(base_angle*no_of_image))
            angle_y = math.sin(math.radians(base_angle*no_of_image))
            x = math.ceil(R * angle_x + 445) + (layers_config.index(layer)*8) #offset to address circles misalignment
            y = math.ceil(R * angle_y + 445) + (layers_config.index(layer)*8) #offset to address circles misalignment
            bg.paste(avatar, (x, y), create_mask(avatar))
            no_of_image += 1
    bg.save('interaction_circle.jpg')
    print('image created and saved')