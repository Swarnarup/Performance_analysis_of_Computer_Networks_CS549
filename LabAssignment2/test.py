import subprocess

if __name__ == "__main__":
    device_name = "ens33"
    inp = input("start namespace creation (y/N)")
    
    nmSpaces = ["NetNsA", "NetNsB", "NetNsC", "NetNsD"]
    
    macvlans = []
    ipAdds = []

    for i in range(len(nmSpaces)):
        macvlans.append(f"macvlan{i+1}")
        ipAdds.append(f"192.0.2.{i+1}/24")
    
    if(inp in "yY"):
        print("Creating network namespaces -->>")
        for i in nmSpaces:
            print(f"sudo ip netns add {i}")
            subprocess.run(f"sudo ip netns add {i}", shell=True)

            
        print("Creating macVLANs -->>")
        for i in macvlans:
            print(f"sudo ip link add {i} link {device_name} type macvlan mode bridge")
            subprocess.run(f"sudo ip link add {i} link {device_name} type macvlan mode bridge", shell=True)
            

        print("Assigning macVLANs to nmSpaces -->>")
        for i in range(len(nmSpaces)):
            print(f"sudo ip link set {macvlans[i]} netns {nmSpaces[i]}")
            subprocess.run(f"sudo ip link set {macvlans[i]} netns {nmSpaces[i]}", shell=True)


        print("Assigning ip to macVLANs -->>")
        for i in range(0, len(nmSpaces)):
            print(f"sudo ip netns exec {nmSpaces[i]} ifconfig {macvlans[i]} {ipAdds[i]}")
            subprocess.run(f"sudo ip netns exec {nmSpaces[i]} ifconfig {macvlans[i]} {ipAdds[i]}", shell=True)



    inp = input("start cleaning (y/N)")
    if(inp in "yY"):
        print("cleaning namespaces  -->>")
        for i in range(len(nmSpaces)):
            print(f"sudo ip netns delete {nmSpaces[i]}")
            subprocess.run(f"sudo ip netns delete {nmSpaces[i]}", shell=True)