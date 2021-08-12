## 使用说明


### 安装
```.bash
pip install -r requirements.txt
```

在python3.6环境下测试


### 推理
```.bash
sh run_bert_ctc2021.sh
```

### 训练
1. 将训练集train.json中数据分成两个文件，train.src和train.tgt  
2. 使用tokenizer.py或其他工具将数据进行分词  
3. 使用预处理脚本将数据处理成gecotr需要的格式  
```
python utils/preprocess_data.py -s SOURCE -t TARGET -o OUTPUT_FILE
```
4. 使用stage1_bert_ctc2021.sh训练模型  


### 评测
```
python evaluate.py -i input_file -r reference_file -p predict_file
```
