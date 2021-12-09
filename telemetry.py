

def main():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temperature = f.read()/100;
        print (temperature)

if __name__ == "__main__":
    main()