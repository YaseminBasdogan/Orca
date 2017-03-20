import sys
import OrcaLibrary as ol

#/ihome/jkeith/yab16/ORCA/GasPhase

for file in sys.argv[1:]:
    file_name = file.split('.')[0]
    output_file = open(file, 'r')
    energy_Values = []
    file_Names = []
    converged = False
    for line in output_file:
        if 'THE OPTIMIZATION HAS CONVERGED' in line:
            converged = True
        if 'FINAL SINGLE POINT ENERGY' in line:
            energy = line.split()
            energy_Values.append(energy[4])
            file_Names.append(file_name)
    output_file.close() 

    if(not converged):
        step, GEO = ol.LAST_GEO(file)
        print '{0} ran to step {1} and did not converge, created restart coordinates.'.format(file, step)
        inp_file = open(file.split('.')[0] + '.inp', 'r')
        rst_file = open(file.split('.')[0] + '_rst.inp', 'w')

        copy_flag = True
        for line in inp_file:
            if copy_flag == True:
                rst_file.write(line)
            if '* xyz ' in line:
                copy_flag = False
        
        for atom in GEO:
            rst_file.write(atom)
        rst_file.write('*')
        rst_file.close()
    
if(converged):
    summary_file = open('energy_summary.txt', 'w')
    index = len(energy_Values) - 1
    summary_file.write(file_Names[index] + ' ' + energy_Values[index] + '\n')
    #for i in range(len(energy_Values)):
    #    summary_file.write(file_Names[i] + ' ' + energy_Values[i] + '\n')
    summary_file.close() 
else:
    summary_file = open('energy_summary.txt', 'w')
    index = len(energy_Values) - 1
    summary_file.write(file_Names[index] + ' ' + energy_Values[index] + '\n')
    summary_file.close()
