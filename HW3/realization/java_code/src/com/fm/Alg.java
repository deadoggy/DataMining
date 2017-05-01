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
            aprSet = apriori.runAlgorithm(1.0, "dataItem", "aprRes");
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

            //开始时间
            Date begTime = new Date();
            fpSets = fpgrowth.runAlgorithm("dataItem", "fpRes", 1.0D);
            //结束时间
            Date endTime = new Date();

            fpTime = endTime.getTime() - begTime.getTime();

            System.out.println("fpTime:" + fpTime);
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    private static void generateTimeSeqFile(){
        try{
            //输入文件
            File dataItemFile = new File("dataItem");
            BufferedReader input = new BufferedReader(new FileReader(dataItemFile));
            //输出文件
            File timeSeqFile = new File("timeSeq");
            FileWriter out = new FileWriter(timeSeqFile);
            //把数据处理成时间序列格式
            String line;
            while((line = input.readLine()) != null){
                String[] items = line.split(" ");
                StringBuilder outLine = new StringBuilder();
                for(String item : items){
                    outLine.append(item);
                    outLine.append(" ");
                    outLine.append("-1 ");
                }
                outLine.append("-2\n");
                out.write(outLine.toString());
            }
            out.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    private static void runGPS(){
        try{

            //初始化时间序列的数据结构
            boolean outputSequenceIdentifiers = false;
            AbstractionCreator abstractionCreator = AbstractionCreator_Qualitative.getInstance();
            SequenceDatabase sequenceDatabase = new SequenceDatabase(abstractionCreator);
            sequenceDatabase.loadFile("timeSeq", 1.0);
            //生成算法器
            AlgoGSP gsp = new AlgoGSP(1.0, 0, Integer.MAX_VALUE, 0, abstractionCreator);
            //开始时间
            Date begTime = new Date();
            //跑算法
            gsp.runAlgorithm(sequenceDatabase,true,false,"gpsRes", outputSequenceIdentifiers);
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
            //初始化时间序列结构
            ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.dataStructures.creators.AbstractionCreator
                    abstractionCreator = ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.dataStructures.creators.AbstractionCreator_Qualitative.getInstance();

            IdListCreator idListCreator = IdListCreator_FatBitmap.getInstance();

            CandidateGenerator candidateGenerator = CandidateGenerator_Qualitative.getInstance();

            ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.dataStructures.database.SequenceDatabase
                    sequenceDatabase = new ca.pfv.spmf.algorithms.sequentialpatterns.spade_spam_AGP.dataStructures.database.SequenceDatabase(abstractionCreator, idListCreator);

            sequenceDatabase.loadFile("timeSeq", 1.0);
            //生成算法器
            AlgoSPADE spade = new AlgoSPADE(1.0, true, abstractionCreator);
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

    public void runAll(){
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置日期格式
        System.out.println(df.format(new Date()));// new Date()为获取当前系统时间
        System.out.println("Apriori alg");
        Alg.runApriori();
        System.out.println("FPGrowth alg");
        Alg.runFPGrowth();
        System.out.println("GPS alg");
        Alg.runGPS();
        System.out.println("SPADE alg");
        Alg.runSPADE();
        System.out.println(df.format(new Date()));// new Date()为获取当前系统时间
    }
    public static void main(String[] argv){
        Alg alg = new Alg();
        alg.runAll();
    }
}
