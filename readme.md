Introduction to Wireless and Mobile Networking: Final Project
===

## <font color=red>Proposal</font>

1. 研究buffer中drop封包的機制，而buffer可以是每個BS(Base station)就maintain一個大buffer for所有底下的UE(user equipment)，或是BS為每個UE準備各一個小buffer，這樣每個小buffer就按照設計的演算法做封包的drop，若BS只有一個大buffer，那我們可以設定forward封包的規則，可能是根據UE的priority(reliability方面)，然後可以討論UE數量對於forward封包規則後的performance(error rate)。


>* First in first out (FIFO)
>* round-robin (RR)
>* earliest deadline first (EDF)
>* shortest job first (SJF)
>* multilevel priority queue
>* ~~preemptive shortest job first (PSJF)~~


>>＊error rate:
>>>-UE
>>>-BS
>>>

>>>#data 

2. (Load Balanced) 
   延伸之前作業的handover,在handover前除了判定SINR 的threshold,再近一步比較要漫遊到的BS,其load是否足以負荷多連接一個UE,所以這樣要maintain每個BS底下有多少UE。
   
3. 