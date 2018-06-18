#!/bin/bash

echo "debut" > trace_auto_reboot
sleep 30

#boucle 
while [ 1 ]
do
  en_cours=$(ps -aux | grep "python3 supervisor" | grep -v "grep" | wc -l)
  #echo "en_cours = " $en_cours >> trace_auto_reboot
  
  if  [ $en_cours != 1 ]
  then
     #echo "a relancer : " $en_cours >> trace_auto_reboot
     reboot
  else
     #echo "en cours : "  $en_cours >> trace_auto_reboot
  fi

  # attente
  sleep 5
done


echo "fin" >> trace_auto_reboot
