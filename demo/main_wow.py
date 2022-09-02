from ext_alg.WOW import demo_wow_embed

if __name__ == '__main__':
    path = '../demo/test_data/test1_sm.png'  # image path
    secret = 3521               # payload(bits per pixel)
    demo_wow_embed(path, secret)
