

def main():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temperature = int(f.read())/1000
        print (temperature)

if __name__ == "__main__":
    main()