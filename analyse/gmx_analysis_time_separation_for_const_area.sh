source /home/maryamma/softwares/gmx/2024.1/bin/GMXRC

# directories=("2fs" "deform/10-4" "deform/10-4/eq/0.20" "deform/10-4/eq/0.35m" "deform/10-4/eq/0.45m")
directories=("deform/10-4/eq/0.45m") # ("deform/10-4" "deform/10-4/eq/0.20" "deform/10-4/eq/0.35m" "deform/10-4/eq/0.45m")

source_dir="/run/media/maryamma/One Touch/project_md/project_2/gromacs/"
cd "$source_dir"
pwd
analyse_dir='analyse'
for dir in "${directories[@]}"
do 
	simulation="${dir##*/}"
	cd $dir
	pwd
	if [ ! -d $analyse_dir ]
	then
		mkdir $analyse_dir || exit
	# else 
		# rm $analyse_dir/*
	fi
	# for sims in "${simulations[@]}"
	# do 
	# 	cd $sims
	# 	pwd
	for time in $(seq 0 1000 199000)
	do
		end=`expr $time + 1000`
		echo 1 | gmx density -f $simulation.xtc -s $simulation.tpr -b $time -e $end -o $time-$end-densityprot
		gmx analyze -f sasa-protmemb.xvg -ee $analyse_dir/$time-$end-analyse-sasa-protmemb.xvg -b $time -e $end > gromacs.out
		gmx analyze -f gyrate-membprot.xvg -ee $analyse_dir/$time-$end-analyse-gyrate-membprot.xvg -b $time -e $end > gromacs.out
		gmx analyze -f hbnum-membprot.xvg -ee $analyse_dir/$time-$end-analyse-hbnum-membprot.xvg -b $time -e $end > gromacs.out
	done
	# 	cd ../../
	# done
#	cd "fast/"
#		# pwd
#		gmx analyze -f ten.xvg -ee analyse-ten.xvg
#		cd ../
	cd "$source_dir"
done


