#include "kmers.cuh"
#include "ffpKmersLib.cuh"
#include <string>

namespace kmerslib{

    int makeFFPS(std::string prefixDirName,int startk, int endk, int deviceN){
    //    int main(int argc, char *argv[]){    
        
            std::vector<string> filename;//Vector Contain each name present in the specific directory 
            std::vector<string> nameOut;
            std::vector<string> fileSequenceName;
            std::vector<int> TotalString;//Vector to save total string for each sequence
            // std::vector<string> name, content;//Variable content have all nucleotides present in one sequence file
            //Read files in the directory
            //string prefixNameN;
            //int begin,Stop;
            /*if (argc>1)
                prefixName = argv[1];
            else{
                cout<<"Proporciona el nombre del Directorio: ";
                cin >> prefixName;
            }*/
            //prefixNameN=prefixName;
            string ndir=prefixDirName;
            cout<<"Directorio de trabajo "<<ndir<<endl;
            //string ndir="/home/may/Genomas/Acholeplasmatales";
            //string ndir="/home/may/Genomas/alone";
            //string ndir="/home/may/GenBank/FamiliesFiles/"+ prefixNameN;
            //char ndir[]={"./Enterobac"};// SequencesP SequenceN GenDivi403Fr SequenceN_403 Contig Scaffold Chromosome Rangos analisys NoConocido GenSingle GenMultiWN Enterobac
            if (readDirectory(ndir.c_str(),filename,nameOut) != 0)
            {
                cout <<"ERROR de Lectura de Directorio "<<endl;
                return 0;
            }
            //int startk=3, endk=20;
                
            //Vector con los lmers y las probabilidades calculadas estas contenidas en una structura 
            //thrust::host_vector<DataSequences *> dna(filename.size());
            
            
        //Process n files, converter secuences string to secuences integer
        /*string fList= "/home/may/crossPlatform/listFiles.txt";//listHafniFam.txt listCincoFam.txt listFileAll.txt
        std::vector<string> nameF, contentF;
        if (readSecuenceFile2(fList, nameF)!=0){
            cout<<"File Reading Error in I: "<<fList<<endl;
        }else{
                cout<<"+++++++++++++ "<<nameF.size()<<endl;
                cout<<"File NAME "<<filename.size()<<endl;
                for (int ll=0;ll<filename.size();ll++){
                    cout<<" NF "<<nameF[ll] <<endl;
                    cout<<" VF "<<filename[ll] <<endl<<endl;
                }
                cout<<" Pulsar Para Calcular los CRES "<<endl<<endl;      
                getchar();   
                filename.resize( nameF.size());
                //filename=nameF;
        }*/
            //int begin;//,Stop;
            std::vector<string> name, content;
            float elapsedTime;
            string dirfilelog="./";
            string prefixName="Out_";
            calculateAllFFPs(deviceN,startk, endk, filename,elapsedTime, dirfilelog, prefixName);
            //calculateAllFFPs(0,13, 16, filename,elapsedTime, dirfilelog, prefixName);
            cout << endl <<"Tiempo de ejecucion fpp " << elapsedTime <<" ms" <<endl;
            return 1;
        }

}