L = 130 # Front axis length in mm
vm_off = -280.0/3  # actual robot velocity offset in mm/s 
scale = 10    # mapping factor between motor speed and wheel linear velocity
NEG = True   # whether car motion in backward
vml = np.array(n * [40])  # left motor commanded speed (speed range: 20 - 100)
vmr = np.array(n * [40])  # right motor commanded speed (speed range: 20 - 100)
vl = np.add(vml*scale, n * [vm_off]) # Left wheel linear velocity in mm/s
vr = np.add(vmr*scale, n * [vm_off]) # Right wheel linear velocity in mm/s
if NEG:
  vl = -vl
  vr = -vr
