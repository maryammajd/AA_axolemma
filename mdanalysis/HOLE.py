from MDAnalysis.analysis import hole2
profiles = hole2.hole('/run/media/maryamma/One Touch/project_md/project_2/gromacs/2fs/7-3.gro', executable='/home/maryamma/softwares/hole2-ApacheLicense-2.2.005-Linux/hole2/exe/hole')
# to create a VMD surface of the pore
hole2.create_vmd_surface(filename='hole.vmd')
