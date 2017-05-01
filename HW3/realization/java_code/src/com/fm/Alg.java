package com.fm;

import ca.pfv.spmf.algorithms.frequentpatterns.apriori.AlgoApriori;
import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowth;
import ca.pfv.spmf.algorithms.sequentialpatterns.gsp_AGP.AlgoGSP;
import ca.pfv.spmf.algorithms.sequentialpatterns.gsp_AGP.items.SequenceDatabase;
import ca.pfv.spmf.algorithms.sequentialpatterns.gsp_AGP.items.creators.AbstractionCreator;
import ca.pfv.spmf.algorithms.sequentialpatterns.gsp_AGP.items.creators.AbstractionCreator_Qualitative;
import ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.AlgoSPADE;
import ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.candidatePatternsGeneration.CandidateGenerator;
import ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.candidatePatternsGeneration.CandidateGenerator_Qualitative;
import ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.idLists.creators.IdListCreator;
import ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.idLists.creators.IdListCreator_FatBitmap;
import ca.pfv.spmf.patterns.itemset_array_integers_with_count.Itemsets;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

/**
 * Created by deadoggy on 17-5-1.
 */
public class Alg {
    private static Itemsets aprSet;
    private static Long aprTime;
    private static Itemsets fpSets;
    private static Long fpTime;
    private static Long gspTime;
    private static Long spadeTime;

    private static void runApriori(){
        try{
            AlgoApriori apriori = new AlgoApriori();
            //开始时间
            Date begTime = new Date();
            aprSet = apriori.runAlgorithm(0.5, "dataItem", "aprRes");
            //结束时间
            Date endTime = new Date();

            aprTime = endTime.getTime() - begTime.getTime();
            System.out.println("aprTime:" + aprTime);

        }catch(Exception e){
            e.printStackTrace();
        }

    }

    private static void runFPGrowth(){
        try{
            AlgoFPGrowth fpgrowth = new AlgoFPGrowth();
            //截取数据
            String dataFileName = "fpgData";
            divideData(30,dataFileName);
            //开始时间
            Date begTime = new Date();
            fpSets = fpgrowth.runAlgorithm(dataFileName, "fpRes", 1.0D);
            //结束时间
            Date endTime = new Date();

            fpTime = endTime.getTime() - begTime.getTime();

            System.out.println("fpTime:" + fpTime);
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    private static void runGSP(){
        try{
            //截取数据
            String dataFileName = "gspData";
            generateTimeSeqFile(30, dataFileName);
            //初始化时间序列的数据结构
            boolean outputSequenceIdentifiers = false;
            AbstractionCreator abstractionCreator = AbstractionCreator_Qualitative.getInstance();
            SequenceDatabase sequenceDatabase = new SequenceDatabase(abstractionCreator);
            sequenceDatabase.loadFile(dataFileName, 0.5);
            //生成算法器
            AlgoGSP gsp = new AlgoGSP(0.5, 0, Integer.MAX_VALUE, 0, abstractionCreator);
            //开始时间
            Date begTime = new Date();
            //跑算法
            gsp.runAlgorithm(sequenceDatabase,true,false,"gspRes", outputSequenceIdentifiers);
            //结束时间
            Date endTime = new Date();

            gspTime = endTime.getTime() - begTime.getTime();

            System.out.println("gspTime:" + gspTime);

        }catch(Exception e){
            e.printStackTrace();
        }
    }

    private static void runSPADE(){
        try{
            //截取数据
            String dataFileName = "spadeData";
            generateTimeSeqFile(30, dataFileName);

            //初始化时间序列结构
            ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.dataStructures.creators.AbstractionCreator
                    abstractionCreator = ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.dataStructures.creators.AbstractionCreator_Qualitative.getInstance();

            IdListCreator idListCreator = IdListCreator_FatBitmap.getInstance();

            CandidateGenerator candidateGenerator = CandidateGenerator_Qualitative.getInstance();

            ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.dataStructures.database.SequenceDatabase
                    sequenceDatabase = new ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.dataStructures.database.SequenceDatabase(abstractionCreator, idListCreator);

            sequenceDatabase.loadFile(dataFileName, 0.5);
            //生成算法器
            AlgoSPADE spade = new AlgoSPADE(0.5, true, abstractionCreator);
            //开始时间
            Date begTime = new Date();
            //跑算法
            spade.runAlgorithm(sequenceDatabase, candidateGenerator, true, false,"spadeRes",false);
            //结束时间
            Date endTime = new Date();

            spadeTime = endTime.getTime() - begTime.getTime();

            System.out.println("spade:" + spadeTime);

        }catch(Exception e){
            e.printStackTrace();
        }
    }

    private static boolean divideData(Integer dataSum, String fileName){
        try{
            // source file
            File sourceFile = new File("dataItem");
            BufferedReader sourceReader = new BufferedReader(new FileReader(sourceFile));
            // target file
            File targetFile = new File(fileName);
            FileWriter targetWriter = new FileWriter(targetFile);
            String line;
            // read from source file
            while((line = sourceReader.readLine()) != null){
                String[] pts = line.split(" ");
                for(int i=0; i<dataSum; i++){
                    targetWriter.write(pts[i]);
                    if(i != dataSum -1){
                        targetWriter.write(" ");
                    }else{
                        targetWriter.write("\n");
                    }
                }

            }
            sourceReader.close();
            targetWriter.close();
            return true;
        }catch(Exception e){
            e.printStackTrace();
            return false;
        }

    }

    private static void generateTimeSeqFile(int dataSum, String fileName){
        try{
            //输入文件
            File dataItemFile = new File("dataItem");
            BufferedReader input = new BufferedReader(new FileReader(dataItemFile));
            //输出文件
            File timeSeqFile = new File(fileName);
            FileWriter out = new FileWriter(timeSeqFile);
            //把数据处理成时间序列格式
            String line;
            while((line = input.readLine()) != null){
                int flag = 0;
                String[] items = line.split(" ");
                StringBuilder outLine = new StringBuilder();
                for(String item : items){
                    outLine.append(item);
                    outLine.append(" ");
                    outLine.append("-1 ");
                    //如果数据数量到达上限就退出
                    flag ++;
                    if(flag == dataSum){
                        break;
                    }
                }
                outLine.append("-2\n");
                out.write(outLine.toString());
            }
            out.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public void runAll(){
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置日期格式
        System.out.println(df.format(new Date()));// new Date()为获取当前系统时间
        System.out.println("Apriori alg -- 1000");
        Alg.runApriori();
        System.out.println("FPGrowth alg -- 30");
        Alg.runFPGrowth();
        System.out.println("GPS alg -- 30");
        Alg.runGSP();
        System.out.println("SPADE alg -- 30");
        Alg.runSPADE();
        System.out.println(df.format(new Date()));// new Date()为获取当前系统时间
    }
    public static void main(String[] argv){
        Alg alg = new Alg();
        alg.runAll();

    }
}
