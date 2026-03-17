import pysilk, lameenc, os


output = f"{os.path.dirname(__file__)}\\output"

def _pcm_to_mp3(pcm_path, mp3_path, sample_rate=48000, channels=1, bits_per_sample=128):
    # Validate input file
    if not os.path.isfile(pcm_path):
        raise FileNotFoundError(f"PCM file not found: {pcm_path}")
    else:
        print(f"File will save as {mp3_path}")
    # Read PCM data
    with open(pcm_path, "rb") as f:
        pcm_data = f.read()
    # Initialize LAME encoder
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(bits_per_sample)  # kbps
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(channels)
    encoder.set_quality(2)  # 2 = high quality, slower

    # Encode PCM to MP3
    mp3_data = encoder.encode(pcm_data)
    mp3_data += encoder.flush()

    # Save MP3 file
    with open(mp3_path, "wb") as f:
        f.write(mp3_data)
    
    print("MP3 File saved")

    # Clean up temporary PCM file
    try:
        os.remove("temp/temp.pcm")
        os.rmdir("temp")
        print(f"Temp File Clear")
    except FileNotFoundError: print("Temp file not found")
    except Exception as e: print(e)

def amr_to_mp3(fileName, inPath = None, outPath = output, output = None):
    try:
        os.mkdir("temp")
    except FileExistsError: pass
    if inPath != None: file = f"{inPath}\\{fileName}"
    else: file = fileName
    with open(file, "rb") as silk, open("temp/temp.pcm", "wb") as pcm:
        pysilk.decode(silk, pcm, 48000)
    print(f"File {fileName} converted to pcm file")
    if output == None: output = f"{fileName[:fileName.rfind(".")]}.mp3"
    if outPath != None: output = f"{outPath}\\{output}"
    _pcm_to_mp3("temp/temp.pcm", output)


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    files = os.listdir(path)
    output = path
    if "input" in files:
        files = os.listdir(f"{path}\\input")
        output = f"{path}\\output"
        try: os.mkdir("output")
        except FileExistsError: pass
        path = f"{path}\\input"
        print("Input Folder Found, Input Detect Action Will Change Into Input Folder")
    
    print("Start to detect file\n")
    for file in files:
        if file[-4:] == ".amr" or file[-5:] == ".silk":
            print(f"File {file} detected")
            try:
                amr_to_mp3(file, inPath = path, outPath = output)
            except: print(f"File {file} convert failed")
            print(f"Convert complete\n")
    print("Convert completed")