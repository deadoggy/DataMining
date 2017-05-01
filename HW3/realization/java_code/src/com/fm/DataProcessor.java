package com.fm;


import java.io.*;
import java.util.*;

class DataProcessor{

    public static void main(String[] argv){
        try{
            // 数据上限
            int upBound = 1000;
            // 文件列表
            String[] fileList = {"new4gtest.csv", "new4gtrain.csv"};
            // item记录
            Map<Integer, List<Integer>> item = new HashMap<Integer,List<Integer>>();
            // 从每个文件中提取数据
            for (String fileName : fileList){
                File dataCSV= new File(fileName);
                BufferedReader input = new BufferedReader(new FileReader(dataCSV));
                //去掉首行
                String line = input.readLine();
                int pos = 0;
                while(null != (line = input.readLine()) && pos < upBound){
                    pos++;
                    //获取手机ID 和 栅格ID
                    String[] attributes = line.split(",");
                    Integer phoneId = Integer.parseInt(attributes[1]);
                    Integer gridId = Integer.parseInt(attributes[47]);
                    // 计入到map里
                    if(item.containsKey(phoneId)){
                        item.get(phoneId).add(gridId);
                    }else{
                        List<Integer> trace = new LinkedList<>();
                        trace.add(gridId);
                        item.put(phoneId,trace);
                    }
                }
            }
            System.out.print("Out\n");
            // 输出文件
            File outFile = new File("dataItem");
            FileWriter out = new FileWriter(outFile);
            // 把item输出到文件
            for(Integer key: item.keySet()){
                System.out.println("key: "+key);
                List<Integer> trace = item.get(key);
                StringBuilder traceStr = new StringBuilder();
                System.out.println(trace.size());
                for(int i=0; i<trace.size(); i++){
                    System.out.println(i);
                    traceStr.append(trace.get(i).toString());
                    if(i != trace.size()-1){
                        traceStr.append(' ');
                    }else{
                        traceStr.append('\n');
                    }
                }
                out.write(traceStr.toString());
            }
            out.close();
        }catch(Exception e){
            e.printStackTrace();
        }

    }

}