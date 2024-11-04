# download mujoco200
`wget https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz`

# extract mujoco200
`tar -xvzf mujoco210-linux-x86_64.tar.gz`

# add mujoco200 to ~/.bashrc
`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/fandes/workspace/mujoco210/bin`

# compile urdf to xml
`compile ./urdf/biped_s3_for_xml.urdf ./urdf/biped_s3.xml`

# note:
- you need to use stl instead of obj files for the visual meshes in the urdf file, you can use meshlab to convert stl to obj
- the number of faces should be between 1 and 200000 in STL
