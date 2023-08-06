#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cuda.h>
#include <cuda_runtime.h>
#include <math.h> 
#include <time.h> 
#include <sstream> 
//#include <map>

#include <thrust/system_error.h>
#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/reduce.h>
#include <thrust/unique.h>
#include <thrust/sort.h>
#include <curand_kernel.h>
//#include <thrust/random.h>
#include <thrust/extrema.h> //libreria para buscar el maximo valor en el vector
#include <thrust/find.h>
#include <thrust/merge.h>
#include <thrust/execution_policy.h>
//Libs for read directory
#include <sys/types.h>
#include <dirent.h>
#include "book.h"
#include "structure.h"
#include "gputools.h"
//#include "utiltools.h"
//#include "statistical.h"
using namespace std;


//********* datos para guardar los tiempo de ejecucion
 //stringstream strtemp;
 //strtemp<<sizeString;
 //string timeofRun="./Resultados/Tiempos.txt";
 //ofstream fileOutT (timeofRun.c_str());    
//***********

//function to read secuence file
int readSecuenceFile(string filename, std::vector<string>  &nameT, std::vector<string> &contentT)
{
    //open file if the file present a problem when opened return -1 
    ifstream input(filename.c_str());
    if(!input.good()){
        std::cerr << "Error opening '"<<filename<<"'. Bailing out." << std::endl;
        return -1;
	//exit();
    }
 
    std::string line, content,name;//, name, content;
    //int frac=0;
    //extract line by line and the result assign in content variable and the header file content in name variable
    while( std::getline( input, line ).good() ){
         //frac++;
        if( line.empty() || line[0] == '>' ){ // check if line is empty or the first character is > that mean the line is the name of the secuence
	        if( !name.empty()){ // check when the file have more than one secuence
                contentT.push_back (content);
		        name.clear();//Clear name variable for if exist other secuence
                content.clear();//Clear de content for the file have other secuence
		        //cout<<" Entrance if name  "<<endl; 
		        //std::cout << "Size "<< content.size() <<std::endl;
	      
	        }
            if(!line.empty()){
	            //cout<<" Entrance if line"<<endl; 
	            name=line;
                //std::cout << name << " :: " <<" "<<!name.empty() <<endl;
                nameT.push_back (line); //Delete the first character in the header secuence, the character is >
            }
        } else if( !name.empty() ){ //Check when the name content the header of the file secuence                
                  line.erase(line.size());
		          content += line;//this line is when the line add to content
                }
    } 
    if(content.size()>0)
       contentT.push_back (content);
    
    input.close();//Close file
    return 0;
}


int readSecuenceFile2 (string filename, std::vector<string>  &nameT){
    //open file if the file present a problem when opened return -1 
    ifstream input(filename.c_str());
    if(!input.good()){
        std::cerr << "Error opening '"<<filename<<"'. Bailing out." << std::endl;
        return -1;
	//exit();
    }
 
    std::string line, content,name;//, name, content;
    //int frac=0;
    //extract line by line and the result assign in content variable and the header file content in name variable
    while( std::getline( input, line ).good() ){
        
                //std::cout << name << " :: " <<" "<<!name.empty() <<endl;
                nameT.push_back (line);//Delete the first character in the header secuence, the character is >
           }
  input.close();//Close file
   return 0;
}


//******* Function to return memory to the deviece
void clearMemory(thrust::host_vector< datasRange *> &Ranges, thrust::host_vector< datasCrude *> &Datas)
{ 
    for(int x=0;x<Ranges.size();x++){
        Ranges[x]->dataRange.clear();
        thrust::host_vector<int>().swap(Ranges[x]->dataRange);  
        Datas[x]->dataCrude.clear();  
        thrust::host_vector<int>().swap(Datas[x]->dataCrude);  
    }
    Ranges.clear();
    thrust::host_vector<datasRange *>().swap(Ranges);
    Datas.clear();
    thrust::host_vector<datasCrude *>().swap(Datas); 
}//******* End the function to return memory to the deviece

//Function to read all name of file (s) present in the directory 
int readDirectory(string namedir,std::vector<string> &filename,std::vector<string> &namesout){
  // Directory to read files name
  DIR *dir;
  //  *ent structure to open file information one by one 
  struct dirent *ent;

  dir = opendir (namedir.c_str());
  // check to error dir 
  if (dir == NULL){
    perror ("No puedo abrir el directorio");
    return -1;
  }
  // Read files one by one 
  while ((ent = readdir (dir)) != NULL)
    {
      //  (.) actual directory and  (..) previous directory
      if ( (strcmp(ent->d_name, ".")!=0) && (strcmp(ent->d_name, "..")!=0) ){
	  // save name in vector 
	  filename.push_back (namedir + "/" + string(ent->d_name));
          namesout.push_back (string(ent->d_name));
      }  
    }
   //Close directory
  closedir (dir);
  return 0;
}
// Function to calculate the edge of each sequence that containing valid nucleotides
int splitSequence(std::vector<string> &content, thrust::host_vector< datasRange *> &Ranges, thrust::host_vector< datasCrude *> &Datas)
{
    //++++Process to jump N values present into genome file+++++++++++++++++++ 
    int totNucleotides=0; 
    for(int ii=0;ii< content.size();ii++){
        //extract line by line and the result assign in content variable and the header file content in name variable
        //fileSequenceName.push_back (name);
        //cout<<"Procesando la "<<ii<<" parte del archivo en turno que tiene "<<content.size()<<endl<<endl;
        int totElement =content[ii].size()+2;//totElement is use to conculate the number of the block need            
        //cout<<content<<endl;            
        thrust::device_vector< char> dataSecuenceStr(totElement);//vector contain the string present in file
        thrust::device_vector< int> dataSecuenceInt(totElement,0);//vector contain the converter value for each character present in dataSecuenceStr
        //dnasInt[i]=new intSequences (totElement);
                    
        //Calculate the number of blocks need to run in parallel
        int threadsPerBock=1024;//number of threads Per Bock
        int blocksPerGrig = (totElement+(threadsPerBock-1))/threadsPerBock;//number of block
                        
        //cout <<"Total de nucleotidos "<<totElement<<" --> "<<endl;//<<(totElement+(threadsPerBock-1)/threadsPerBock)<<endl;
        //fileOutT<<"Total de nucleotidos "<<totElement<<" --> "<<endl;

        //Copy string content in a character vector that it will be converted into a number vector.
        thrust::copy (content[ii].begin(),content[ii].end(),dataSecuenceStr.begin()+1);
        dataSecuenceStr[0]='A';//Add to complete the padding at first position 
        dataSecuenceStr[totElement-1]='A';//Add to complete the padding at last position 
        content[ii].clear();
        
        //Call  the function that determines the edge of each segment of sequence in GPU
        char *pd_vecStr = thrust::raw_pointer_cast(dataSecuenceStr.data());//To determine the memory position in the GPU device
        int *pd_vecInt = thrust::raw_pointer_cast(dataSecuenceInt.data());//To determine the memory position in the GPU device    
                    
        //Call function for converter vector str to binary vector  
              //blocks number, threads per block
        markNs<<<blocksPerGrig,threadsPerBock>>>(pd_vecStr, pd_vecInt, totElement);
        cudaDeviceSynchronize();
                    
        dataSecuenceInt[0]=0;
        dataSecuenceInt[totElement-1]=0;
        //cout<<"Frist "<<dataSecuenceInt[0]<<dataSecuenceInt[1]<<" Last "<<dataSecuenceInt[totElement-1]<<endl;
        thrust::device_vector< int> outEdge(totElement,0);
        int *pd_vecoutEdge = thrust::raw_pointer_cast(outEdge.data());
                
        //Call to the function to detect the edge of each trace of sequence
        edgeDetect<<<blocksPerGrig,threadsPerBock>>>(pd_vecInt, totElement,pd_vecoutEdge);
        cudaDeviceSynchronize();
                                 
        //Return memory to GPU device 
        dataSecuenceInt.clear();
        thrust::device_vector<int>().swap(dataSecuenceInt);
        
        cout<<"First edge "<<outEdge[1]<<" Last edge "<<outEdge[totElement-1]<<endl;
        
        //Calculate numbers of N
        //cout <<"Name "<<name[ii]<<" --> "<<endl;
        int Nvalues =totElement-(thrust::count(thrust::device,outEdge.begin(), outEdge.end(),0));                      
        thrust::device_vector<int> Keys(Nvalues,0);
        thrust::copy_if (thrust::device,outEdge.begin(),outEdge.end(),Keys.begin(),is_none());
                    
        //Save keys into their host vector 
        Ranges[ii]=new datasRange(Nvalues);
        Ranges[ii]->dataRange=Keys;
        //Subprocess to determine the total of nucleotides present in each sequence that is contained in the file.
        for(int index=0;index<Ranges[ii]->dataRange.size();index+=2){
            int sizepart =Ranges[ii]->dataRange[index+1]-Ranges[ii]->dataRange[index]+1;
            if(sizepart>=20){
                totNucleotides +=sizepart;
                Ranges[ii]->totNs+=sizepart;
            }
        }
        cout<<"Total of Nucleotides cumulated " <<totNucleotides<<" Total of Nucleotides with characters different from ATCG "<<ii<<" is "<< Ranges[ii]->totNs <<endl;
        cout<<"Pieces " <<Ranges.size()<<endl;
                                                
        //++++ Process to convert the sequence in numbers

        thrust::device_vector< int> dataSecuenceIntr(totElement,0);
        //Call to execute function in GPU
        char *pd_vecStrr = thrust::raw_pointer_cast(dataSecuenceStr.data());//To determine the memory position in the GPU device
        int *pd_vecIntr = thrust::raw_pointer_cast(dataSecuenceIntr.data());//To determine the memory position in the GPU device            
        //Call function for converter vector str to vector int 
        converterStringToInteger<<<blocksPerGrig,threadsPerBock>>>(pd_vecStrr, pd_vecIntr, totElement);
        cudaDeviceSynchronize();
                                 
        //Save dataSequenceStr into their host vector 
        Datas[ii]=new datasCrude(totElement); 
        Datas[ii]->dataCrude=dataSecuenceIntr;   
                
        //To free GPU device memory
        dataSecuenceIntr.clear();
        thrust::device_vector<int>().swap(dataSecuenceIntr);
                
        //+++++ End Process to convert the sequence in numbers
                
        //Return to memory to GPU device 
        outEdge.clear();
        thrust::device_vector<int>().swap(outEdge);
        Keys.clear();
        thrust::device_vector<int>().swap(Keys);
        dataSecuenceStr.clear();
        thrust::device_vector<char>().swap(dataSecuenceStr);
        cout <<"Total of N "<<(Nvalues/2-1)<<" -->Nvalues"<< Nvalues <<endl;
        cout <<"---------------- CALCULAR Nss Cycle -------->  "<<ii<<" de "<<content.size()<<endl<<endl;		
    }//++++++ End to Process to jump N values present into genomic file ++++++
        
    return totNucleotides;
}//****** End the function to calculate the positions where the sequence has Ns

//******* Function to calculate all strings that have in the sequence without Ns
void calculateAllStrings(int totNucleotides, int sizeString,int startk, thrust::host_vector< datasRange *> &Ranges, thrust::host_vector< datasCrude *> &Datas, thrust::host_vector<DataSequences *> &dna,ofstream &dirfilelog)
{
    int totalString = totNucleotides-sizeString+1;
    thrust::device_vector<unsigned long long int> totKmersSequence(totalString,0);
    cout <<"Total of Nucleotides "<<totNucleotides<<" --> y total de cadenas posibles "<<totalString<<"Tam Vector general "<<totKmersSequence.size()<<endl<<endl;
    int totSeqCopy=0;
    for(int indexseq=0;indexseq<Ranges.size();indexseq++)
    {
        cout <<"......  Processing the subsequence "<<indexseq<<" of KMER "<<sizeString<<"...... and size of genome "<<totKmersSequence.size()<<endl;
        thrust::device_vector<int> dataSecuenceStr(Datas[indexseq]->dataCrude.size());//Variable to copy from host to device
        dataSecuenceStr=Datas[indexseq]->dataCrude;//Move datas form host to device

        //totalString = Ranges[indexseq]->totNs-sizeString+1;//Remeber in the previous process we add 2 values and save Ns number
        //thrust::device_vector<unsigned long long int> totKmersSubSequence(totalString,0);
        cout <<"Total of Nucleotides in CRE "<<Datas[indexseq]->dataCrude.size() <<" and Total of Strings in CRE "<<totalString<<endl<<endl;
        //int totSubSeqCopy=0;
	    for(int index=0;index<Ranges[indexseq]->dataRange.size();index+=2){
            cout <<"......  Processing  the piece "<<index<<" of the subsecuence "<<indexseq<<" of KMER "<<sizeString<<"......"<<endl;
		    int sizePart=Ranges[indexseq]->dataRange[index+1]-Ranges[indexseq]->dataRange[index]+1;//nucleotides number to copy
            cout <<"sizePart "<<Ranges[indexseq]->dataRange[index+1]<<" - "<< Ranges[indexseq]->dataRange[index]<<" = "<< sizePart<<endl;
		    int copyStart= Ranges[indexseq]->dataRange[index];//start to copy at position
		    int copyEnd =Ranges[indexseq]->dataRange[index+1];//end to copy at position
            if(sizePart >= 20){//Each part must be mayor or equal to 20
			    thrust::device_vector<int> partSequence(sizePart);
			    thrust::copy(thrust::device,dataSecuenceStr.begin()+copyStart,dataSecuenceStr.begin()+copyEnd+1,partSequence.begin());
			    cudaDeviceSynchronize();
			    cout <<"Tam piece "<<sizePart<<" start at "<<copyStart<<" end at "<<copyEnd<<endl; 
			    //cout <<"inicio Seq ori "<<Datas[indexseq]->dataCrude[copyStart]<<" el final tiene "<<Datas[indexseq]->dataCrude[copyEnd]<<endl;
			    //cout <<"Dato al final de la copia en "<<"ciclo "<<index<<" es "<<partSequence[sizePart-1]<<endl;
		     	            //N   -    L     +1 
			    totalString = sizePart-sizeString+1; //calculate kmer total  that it's possible to build
			    cout <<"totElement "<<sizePart<<" Total String "<<totalString<<" size of substring "<<sizeString<<endl;
			    dirfilelog<<"totElement "<<sizePart<<" Total String "<<totalString<<" size of substring "<<sizeString<<endl;
			    //*thrust::device_vector<long long int> b(totalString,0);//, *llaves;
			    thrust::device_vector<unsigned long long int> b(totalString,0);//Vector of lmers
			    //TotalString.push_back (totalString);
			    unsigned long long int *pd_vec = thrust::raw_pointer_cast(b.data());//To determine the memory position in the GPU device
			    int *pd_vecInt1 = thrust::raw_pointer_cast(partSequence.data());
			    cout<<"tAM before ffP "<<b.size()<<"and piece is "<< partSequence.size()<<endl;
                //cout << "Antes del FFP"<<endl;
			    //cout <<"Bloques "<<blocksPerGrig<<" Hilos por bloque "<< threadsPerBock<<endl<<endl;
		
			    //Calculate blocks and thread per block need to execute the kernel 
			    int threadsPerBock=1024;//number of thread per bolck
			    int blocksPerGrig = (totalString+(threadsPerBock-1))/threadsPerBock;
				
			    //Call kernel's function to build all kmers possible
			    makeString <<<blocksPerGrig,threadsPerBock>>>(pd_vecInt1, pd_vec,totalString,sizeString);//
			    cudaDeviceSynchronize();

                //Return the device memory
			    partSequence.clear();
			    thrust::device_vector<int>().swap(partSequence);
			    //cout << "despues del FFP"<<endl;
			    //cout <<"pasoFFp "<< i<<endl;
			    cout<<"TAM after ffP "<<b.size()<<endl;
		
			    //----------------------
                cout<<"++++ Copy all words to final vector "<<b.size()<<" Total words "<< totSeqCopy<<endl<<endl;                            
                thrust::copy (thrust::device,b.begin(),b.end(),totKmersSequence.begin()+totSeqCopy);//Copy lmers
		        totSeqCopy+=totalString;
                cout<<"join slice "<<" data it was copy "<< totSeqCopy <<endl; 
                //Return memory
                b.clear();
                thrust::device_vector<unsigned long long int>().swap(b); 
            }//else{//End if subSequence >=20       
            cout<<"++++ Mixing and  the slice was"<<indexseq<<endl;  
              
	    }//End for to process each piece without Ns
        cout<<"*************** Data join is finishing **************++ "<<endl;
    }//End for to process each sequence or plasmid
			  
	//******* The process to count the occurrences to each word that appear in the vector
                           
	//totalString=totKmersSequence.size();//totSeqCopy;
    totalString=totSeqCopy;//totSeqCopy;
    cout<<" Total words "<< totSeqCopy<<" and the size of vector "<< totKmersSequence.size()<<endl;//"PULSA ENTER"<<endl;
    //getchar();
    //Sort Words
	//thrust::sort(totKmersSequence.begin(),totKmersSequence.end());//sort lmer, this is for make easy to calculate unique lmers
    thrust::sort(thrust::device,totKmersSequence.begin(),totKmersSequence.begin()+totSeqCopy);//sort kmer, this is for make easy to calculate unique lmers
	cudaDeviceSynchronize();
	cout <<" Total words "<< totalString<<"and the size of words' vector  together "<< totNucleotides <<endl<<endl;
	dirfilelog<<" Total words "<< totalString<<endl<<endl;

	//thrust::device_vector<int> llaves(totalString,probabilidad);
	thrust::device_vector<unsigned long long int> Keys(totalString,0);//vector to contain each lmer
		                            
	// Use unique` to grab the distinct values  
	//*thrust::device_vector< long long int> values(totalString);
	thrust::device_vector<int> values(totalString,0);//vector to contain occurrences of each lmer
	//cout<<"sort"<<endl;
		
	//cout<<"Copy "<<totKmersSequence.size()<<endl;
		
	//To count the frequencies of all uniques words values
	int rsize = thrust::reduce_by_key(thrust::device,totKmersSequence.begin(), totKmersSequence.begin()+totSeqCopy, thrust::constant_iterator<int>(1), Keys.begin(), values.begin(),equal_key()).first - Keys.begin();
		
	//cout <<"totceros "<<cuantos<<" total cadenas "<< totelemtos<<endl<<endl;
	cout <<" Total Kmers "<< rsize<<endl<<endl;
	//fileOutT<<"totceros "<<cuantos<<" total cadenas "<< totelemtos<<endl<<endl;
	dirfilelog<<" Total Kmers "<< rsize<<endl<<endl;
		
	cout<<"Create Matrix"<<endl;
	//thrust::device_vector< int> templmers(totelemtos);
		
	//Separate unique lmers and ist occurrences in other two vectors
	//int totelemtos = totKmersSequence.size() - rsize;//ELEMENTOS QQUE NO SE DEBEN DE COPIAR
	thrust::device_vector<unsigned long long int> Keys2(rsize,0);//contain unique lmer
	thrust::device_vector<int> values2(rsize,0);//contain values for each unique lmer
	//thrust::copy (Keys.begin(),Keys.end()-totelemtos,Keys2.begin());//Copy lmers
	//thrust::copy (values.begin(),values.end()-totelemtos,values2.begin());//Copy value for each unique lmer 
	thrust::copy (thrust::device,Keys.begin(),Keys.begin()+rsize,Keys2.begin());//Copy lmers
	thrust::copy (thrust::device,values.begin(),values.begin()+rsize,values2.begin());//Copy value for each unique lmer 
	//int frecuenciastot2=thrust::reduce(values2.begin(),values2.end(),0,thrust::plus<int>());
	cout <<" Words Unique "<< Keys2.size()<<endl<<endl;
	//cout<<"conteo de apariciones Tot2 " << frecuenciastot2<<endl;
		
	//Retunr The GPU device memory
	Keys.clear();
	thrust::device_vector<unsigned long long int>().swap(Keys);
	values.clear();
	thrust::device_vector<int>().swap(values);
	totKmersSequence.clear();
	thrust::device_vector<unsigned long long int>().swap(totKmersSequence);
			        
	//To copy the results
	//**************************
	dna[sizeString-startk]=new DataSequences (rsize);
	//dna[i]=new DataSequences (totelemtos);
			 	
	
	dna[sizeString-startk]->kmers=Keys2;
	dna[sizeString-startk]->kmersFreq=values2;
	//double proba=1.0/totalString;
	dna[sizeString-startk]->kmersProbalities=(double)1.0/(double)totalString;
		
	//cout<<"La probabilidad segun chuma es "<<proba<<" y le total de elementos es "<<rsize<<endl;
	//cout<<"tAMAÑO 5 "<<llaves2.size()<<endl;
    
    //Retunr The GPU device memory
	Keys2.clear();
	thrust::device_vector<unsigned long long int>().swap(Keys2);
	values2.clear();
	thrust::device_vector<int>().swap(values2); 
	//cout<<"Primer VALOR  "<<dna[i]->lmers[0]<<" y la probabilidad "<<dna[i]->lmersProbalities<<endl;
	//cout<<"Paso la limpieza del vector 7"<<endl;
	//cout<<"TAMANO VECTORES   "<<dna[i]->lmers.size()<<endl;
	cout <<"Total of correct words "<<dna[sizeString-startk]->kmers.size()  << endl; //" Tam templmers "<< dna[i]->lmers.size()<<endl;
	dirfilelog<<"Total of correct words "<<dna[sizeString-startk]->kmers.size()  <<endl; //" Tam templmers "<< dna[i]->lmers.size()<<endl;

}//******End the function to calculate all strings that have in the sequence without Ns


//******* Function to calculate CRE
void calculateFFP(thrust::host_vector<DataSequences *> &dna, string prefixName,int startk)
{
    
    cout<<"DNA size "<<dna.size()<<endl<<endl;
    //cout<<"K3="<<dna[0]->kmers.size()<<" K4="<<dna[1]->kmers.size();
    for(int i=0;i<dna.size();i++){
	    //++++++++++++++++++++++++++++++++++++++++++++++++++++++
        //Store file with specific kmer and each probablities
        //File to save results
        std::ostringstream ss;
        ss << startk+i;
        string nombref="./FFP_" + prefixName +ss.str()+ ".txt";
        ofstream filecre (nombref.c_str(),ofstream::trunc);
                       //dna[i]->kmers.size()
        for(int pos=0;pos<1000;pos++){
                filecre<<dna[i]->kmers[pos]<<","<<dna[i]->kmersFreq[pos]<<endl;      
        }
        //++++++++++++++++++++++++++++++++++++++++++++++++++++++
        filecre.close();
        dna[i]->kmers.clear();  
	    thrust::host_vector<unsigned long long int>().swap(dna[i]->kmers);
        dna[i]->kmersFreq.clear();  
	    thrust::host_vector<int>().swap(dna[i]->kmersFreq);
        if(i==dna.size()-1) {//Return memory when the k=16 were calculated
            dna[i]->kmers.clear();  
	        thrust::host_vector<unsigned long long int>().swap(dna[i]->kmers);
            dna[i]->kmersFreq.clear();  
	        thrust::host_vector<int>().swap(dna[i]->kmersFreq);
            dna.clear();  
	        thrust::host_vector<DataSequences *>().swap(dna);
         }
		//************************

    }
    //filecre<<endl;
    
    cout<<endl;
    //+++cout<<"Tot CADENAS "<<sunTcad<<" Probabilidad k5 "<<inpro<<" Probabilidad k3 "<<inproSearch<<endl;
        
}//******* End the function to calculate a genome CRE

//Function to calculate all CREs that had been saved in a specified directory
void calculateAllFFPs(int numDevie,int startk, int endk, std::vector<string> &filename, float &elapsedTime, string &dirfilelog,string &prefixName){

    //********* datos para guardar los tiempo de ejecucion
    //stringstream strtemp;
    //strtemp<<sizeString;
    string timeofRun=dirfilelog+"logfile.txt";
    string fileError=dirfilelog+"logerrfile.txt";
    ofstream logF (timeofRun.c_str());
    ofstream logErr (fileError.c_str()); 

    cudaSetDevice(numDevie);//Select device present into the computer
    cudaDeviceReset();//initialize de GPU 
    
    //Check the time
    cudaEvent_t start, stop;
    cout<<"LLEGO al cuda event";
    HANDLE_ERROR( cudaEventCreate(&start));
    HANDLE_ERROR( cudaEventCreate(&stop));
    HANDLE_ERROR( cudaEventRecord(start,0));
    
    cout<<"paso  al cuda event";
    //filename.size()
    for (int i=0;i<filename.size();i++)
    {
        //size_t destination_size = sizeof (filename[i]);
           
        cout<<"Fale name: "<<filename[i]<<endl<<endl; 
        //fileOutT <<filename[i]<<endl;  
        //fileOutT<<"Nombre Archivo: "<<filename[i]<<endl<<endl;

        std::vector<string> name, content; 
        //check have no problem with the file in turn, the file turn is controller for i value
        if (readSecuenceFile(filename[i], name, content)!=0){
            cout<<"Error de Lectura de Archivo: "<<filename[i]<<endl;
            logErr<<"read file fiailed: "<<filename[i]<<endl<<endl;
        }else
        { 
            //cout <<"Total File Sequences "<<content.size()<<" --> "<<endl;
            logF<<"File Name: "<<filename[i]<<endl;
            logF<<"Header File: "<<name[i]<<endl;//c_str()
            logF<<"Total Sequences: "<<content.size()<<endl<<endl;    
            //dataOut[i]=new DataSequences (content.size());   
            //cout<<"tot archi en por cada dir"<<dataOut[i]->lmers.size()<<endl<<endl;            
                 
            thrust::host_vector< datasRange *> Ranges(content.size());
            thrust::host_vector< datasCrude *> Datas(content.size());

            //Calling the function to calculate the position where the sequence has nucleotides different to  ATCG
            int totNucleotides = splitSequence(content, Ranges, Datas); 
                  
            //Return mamory to host
            name.clear();
            vector<string>().swap(name);
            content.clear();
            vector<string>().swap(content);
            //cout<<" Pulsar Para Calcular los K meros "<<endl<<endl;      
            //getchar();
            //+++++ Process to calculate the CRE and union each part of sequence present into each genome
            //cout <<"---------------- CALCULAR LOS KMEROS -------- "<<totNucleotides<<endl;
            logF<<"TOTAL NUCLEOTIDES: "<<totNucleotides<<endl<<endl;
            //+++++++++++++ Process to calculate all kmers from 3 to 25 ++++++++++++++++
            //Vector con los lmers y las probabilidades calculadas estas contenidas en una structura 

            int length=endk-startk+1;//To calculate number of vector that needed for containt each vector words
            thrust::host_vector<DataSequences *> dna(length);
            //        int startk=3, endk=20;

            
            for (int sizeString=startk; sizeString<=endk;sizeString++){
                //total nucleotide 
                //totElement*=2;
                //cout <<"total de elementos por 2  "<< totElement<<endl;
                cout <<"......   KMER Processing at: "<<sizeString<<"......"<<endl;
                //Cut the principal sequence in n parts.
                //cout<<endl <<"Calculando tamaño de secuencia general"<<endl<<endl;
                //Calling the function to assemble all words that were split by the function splitSequence
                calculateAllStrings(totNucleotides, sizeString,startk, Ranges, Datas, dna, logF); 
                
                //cout<<" Pulse ENTER to calculate the K value  "<<sizeString<<endl<<endl;      
                //getchar(); 
            }// End cicle to process kmers between  3 to 20
            
            //Clear memory
            clearMemory(Ranges, Datas);
            
            //Process to calculate CRE from k=5 to k=20
            //string prefixName="SalidaPrue";
            calculateFFP(dna, prefixName,startk);
          }//End else to read genome file
    
    }//End for to process all files present into directory

   
    //++++
    HANDLE_ERROR(cudaEventRecord(stop,0));
    HANDLE_ERROR(cudaEventSynchronize(stop));
 
    //float elapsedTime;
    HANDLE_ERROR(cudaEventElapsedTime(&elapsedTime, start, stop ));
   
    //Destruccion del evento
    HANDLE_ERROR(cudaEventDestroy (start));
    HANDLE_ERROR(cudaEventDestroy (stop));  
 
   
   
    //Imprimir el tiempo de duracion de la ejecucion
    cout << endl <<"Runtime " << elapsedTime <<" ms" <<endl;
    //fileOutT<<endl <<"Tiempo de ejecucion fpp " << elapsedTime <<" ms" <<endl;
   
    //return 0;
}//******* End the function to calculate all CREs present in a vector


//********** Principal function to calculate all CREs to each genome saved in a specific directory  
     //int argc, char *argv[] void
