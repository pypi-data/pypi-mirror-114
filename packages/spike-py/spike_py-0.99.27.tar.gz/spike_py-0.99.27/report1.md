# 1er rapport sur le phasage des 2D.

J'ai travaillé sur les données histonepeptide_2D_00000 $x$ .d avec $x \in \{2, 3, 4, 5\}$ du 4 février

pour rappel

- pulses longs: P1 P2 - 1 µsec/freq et P3 20 µsec/freq
  - histonepeptide_2D_000002 (SwpDir = decreasing *en fréquence !* )
  - histonepeptide_2D_000003 (SwpDir = increasing)
- pulses courts: P1 P2 - 0,5 µsec/freq et P3 1,0 µsec/freq
  - histonepeptide_2D_000004 (SwpDir = increasing)
  - histonepeptide_2D_000005 (SwpDir = decreasing)
 
J'arrive à traiter les 4 2D sans problème avec les `freq_f1demodu` que tu m'as donné *(soit dit en passant, si ils dépendent du balayage en fréquence, et pas de la durée du pulse, c'est bien un problème dans le générateur de fréquence...)*
Les manipes sont propres, avec des fragments à plus haut $m/z$ que les parents.

Par rapport aux durées de pulses p/rp aux fréquence, les ions sont à 220kHz pour les parents et 184kHz pour les fragments. Donc des périodes, de 4.54 µsec et 5.43µsec - et c'est vrai que un balayage à 1 µsec/freq pose peut-être des problèmes...

Bon, pour l'instant je me suis quand même concentré sur les manipes 4 et 5, car je pensais qu'elles sont plus faciles à traiter.

J'ai regardé le premier incrément des 2D, et réussit à les phaser.




## histonepeptide_2D_000004

Dans cette expérience, le premier incrément ne contient pas tous les 

```python

```
