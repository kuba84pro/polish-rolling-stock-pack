Polish Rolling Stock Pack - Read me
=============================

1. About
========
PRSP is a continuation of Polish PKP SET 3.0.3 pack made originally by TadeuszD.
It contains most known Polish rolling stock used over the years, since 1918 to the present.

2. Requirements
===============
Minimum OTTD version - 1.14.0
Minimum JGRPP version - 0.59.0

3. Parameters
=============
Polish Rolling Stock Pack supports several parameter:
 1) Disable original trains - selecting this option disables original rail
  engines and wagons for normal tracks. This option don't affects to monorail
  and maglev.
 2) Disable original monorail and maglev trains - selecting this option
  disables original monorail and maglev engines and wagons. Not applicable
  to normal track trains.
 3) Keep old vehicles in purchase menu - selecting this option disables 
  retiring old engines and wagons from purchase menu. Historical vehicles
  will be still available for purchase even on modern ages. This option applies
  only to this set. To disable expiration of vehicles in another NewGRFs use
  option "Vehicles never expire" in game settings.
 4) Transport 'goods' in special wagons - selecting this option allows you
  transport standard cargo 'goods' in special wagons, which are adapted
  by default to transport special cargos defined by FIRS and ECS.
 5) Purchase cost multiplier - this option allow to increase the purchase cost
  of engines and wagons. Applicable only in this set.
 6) Running cost multiplier - this option allow to increase the running cost
  of engines and wagons. Applicable only in this set.

4. Special features
===================

4.1 Brakes in wagons
--------------------
Every train can leave depot only if it has sufficient braking force.
It can be difficult to achieve in earlier times because of lacking brakes
in many old-timer wagons. In case of insufficient braking force you can
increase it by mixing wagons without brakes and wagon with brakes (hand or air).
Usefull notes:
- every engine have its own braking force. It can stop 2 or 3 wagons without
  additional brakes. Bigger engines have  more braking force,
- bigger wagons (4-axles) have more braking force than smaller (2-axles),
- wagons with brakes are more expensive and have more weight.

4.2 Heating in arctic climate
-----------------------------
Passenger trains in arctic climate requires heating. Typically, the heating
power for the train is delivered by the locomotive(s). Passenger wagons
consume this power. We distinguish between two types of heating systems:
- steam
- electric
Some passenger wagons support both systems - steam/electric.
The passenger train can leave the depot only if heating systems of all wagons
and locomotive(s) are compatible and the source of power is sufficient.
In case of insufficient power you can change the locomotive or use special wagon
called 'heating wagon'. This wagon contain steam boiler and produces additional
heating power for steam-heated wagons.

4.3 Restaurant and luggage wagons
---------------------------------
These types of wagons have special purpose. Restaurant coaches (dining cars)
have no possibility to transport passengers. But, included in the train,
restaurant car increases cargo age period for all express coaches included
in the same train. It means that income rate for passenger transportation
in express coaches decreases slower than for coaches in a train without
restaurant car. There is no reason to add more than one restaurant car
per train.
Luggage vans are dedicated for fast transport small portions of goods
for stimulate towns growth. Additionally, similar to restaurant car, luggage van
also increases cargo age period for all express coaches in the same train,
but the effect is less intensive. However restaurant and luggage bonus
are cumulative, so you can add both types of wagons (luggage and restaurant)
to the train to boost the overall efect.

5. Disclaimer
=============
This pack could contain several bugs while playing the game. As much as I possibly could fix them,
I need some time because I'm not a professional programmer and I don't know everything yet.
That means, if you spot something not right, join our discord and report it.

---------------------------------
Don't mix PRSP with PKP set! It could break your save.
---------------------------------