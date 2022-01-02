---
layout: post
title:  "Dactyl Manuform 5x6 Build Log"
date:   2021-12-29 14:23:25 -0400
categories: keyboards, Ergonomics, qmk
---

## Motivation

My main goal for this post is to simply provdie a helpful supplement to other more detailed build guides.  
Many of the build guides I followed while building my dacytl manuform skipped relevant information, 
information critical to the function of the keyboard. My guess is that these guides assumed prior knowledge.  

## Ergonomic Dactyl Kalih Box Navy Jades Build

**Features:**    
Hotswappable  
Key Layout: QWERTY, maybe DVORAK  
QMK Configurable   
Kalih Box Navy   

### Parts and Materials
<style>
.tablelines table, .tablelines td, .tablelines th {
        border: 1px solid black;
        }
</style>
| Parts                       | Specs                            | Count             | Price  | URL                                                                                                                                                                                                                                            |
| ----------------------------|----------------------------------|-------------------|--------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Keyboard Case               | 5x6 Standard with Kalih Hot Swap | 1 order(2 pcs)    | $85.00 | [link](https://www.etsy.com/listing/1028152282/made-to-order-dactyl-manuform?click_key=bc4fa2b252b2076958c924c6f1c3ee0819fec15a%3A1028152282&click_sum=1892a9ae&ref=shop_home_active_2&crt=1&sts=1&variation0=2278401877&variation1=2088216304)|
| Diodes 1N4148               | 2368-1N4148-ND                   | 100 pcs           | $4.24  | [link](https://www.digikey.com/en/products/detail/1N4148/2368-1N4148-ND/11645052?itemSeq=382356410)|
| Kalih Hot-Swappable Sockets | holds switches in place for wiring | 1 order (100 pcs) | $4.24| [link](https://www.amazon.com/Hot-swappable-Socket-CPG151101S11-Mechanical-Keyboard/dp/B096WZ6TJ5/ref=pd_lpo_1?pd_rd_i=B096WZ6TJ5&psc=1)|
| M3 Threaded Inserts         |                                  | 1 order (100 pcs) | $4.24  | [link](https://www.digikey.com/en/products/detail/1N4148/2368-1N4148-ND/11645052?itemSeq=382356410)|
| M3 Screws assortiment       | M3 Comptatible screws            | 1 order (304 pcs) | $9.99  | [link](https://www.amazon.com/Sutemribor-320Pcs-Stainless-Button-Assortment/dp/B07CYNKLT2/ref=sr_1_3?crid=1LLHEMSMGCMXK&keywords=m3+screws&qid=1641085137&s=industrial&sprefix=m3+screws%2Cindustrial%2C76&sr=1-3)|
| Wires                       | Jumper Wires                     | 120 pcs           | $6.98  | [link](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY/ref=sr_1_3?crid=3LNP22FLTTM5C&keywords=EDGELEC+120pcs+Breadboard+Jumper+Wires&qid=1640879388&s=electronics&sprefix=edgelec+120pcs+breadboard+jumper+wires%2Celectronics%2C89&sr=1-3)|
| Elite-C V4                  | USB-C Pro Micro                  | 2 pcs             | $35.98 | [link](https://keeb.io/collections/diy-parts/products/elite-c-low-profile-version-usb-c-pro-micro-replacement-atmega32u4)|
| Key Switches                | NovelKeys x Kaihua Box Navy      | 70 pcs            | $29.40 | [link](https://kbdfans.com/products/novelkeys-x-kailh-box-thick-clicks-navy-jade?variant=2840537759757)|
| TRRS Jack                   | PJ-320A Jack - 3.5mm             | 2 pcs             | $1.00  | [link](https://keeb.io/collections/diy-parts/products/trrs-jack-3-5mm)|
| TRRS Cable                  | B07PJW6RQ7 - 5ft                 | 1 order (2 pcs)   | $6.99  | [link](https://www.amazon.com/Auxiliary-Braided-Compatible-Stereos-Headphones/dp/B07PJW6RQ7/ref=sr_1_2?crid=1RMMTAUNK09NO&keywords=TRRS%2B3.5mm%2BAudio%2BCable&qid=1640881233&s=industrial&sprefix=trrs%2B3.5mm%2Baudio%2Bcable%2Cindustrial%2C80&sr=1-2&th=1)|
| Reset Switch                | Reset Pushbutton Switch          | 2 pc              | $1.00  | [link](https://keeb.io/collections/diy-parts/products/reset-pushbutton-switch)|
| Keycaps                     | Matcha ZDA PBT Keycap set        | 1 order(124 pcs)  | $32.90 | [link](https://www.amazon.com/Similar-Japanese-Russian-Keyboard-Tada68%EF%BC%88Only/dp/B08MDYHJ7Q)|
| PCB (Optional)              | Amoeba Single-Switch PCBs        | 3 order(90 pcs)   | $14.97 | [link](https://keeb.io/collections/diy-parts/products/amoeba-single-switch-pcbs)|
| Rubber Feet                 | Sticky rubber feets              | 1 order (100 pcs) | $3.99  | [link](https://www.amazon.com/dp/B07G8926LH?psc=1&ref=ppx_yo2_dt_b_product_details)|
| Gel wrist rests (Optional)  | Silicone Gel Mouse Pad           | 1 order (2 pcs)   | $15.00 | [link](https://www.amazon.com/LetGoShop-Heart-Shaped-Translucence-Ergonomic-Effectively/dp/B01DKCPC16/ref=pd_yo_rr_rp_5/135-8132732-7350062?pd_rd_w=XFX2T&pf_rd_p=a7b08c2f-223b-4262-a124-eb0a7efa1703&pf_rd_r=D330W5VXKQVKGBC4487N&pd_rd_r=37bc83cd-b13f-4b77-935e-4047d85fb826&pd_rd_wg=TKAfd&pd_rd_i=B01DKCPC16&psc=1)|
| Wrist rests (Optional)      | 3D printed wirst rests           | 1 order (2 pcs)   | $14.00 | [link](https://www.etsy.com/listing/1098507650/pair-of-wrist-rests-for-split-style?click_key=be86e6ce5e47849a9088ed12facff1807e68175e%3A1098507650&click_sum=40716b38&ref=shop_home_active_1&crt=1&sts=1)|

Total Cost excluding optional parts: NaN (Not including shipping and taxes)

### Notes on Materials

* The switches you decide to use will can change your total cost drastically.  
* The key switches is where you want to ball out and pimp your keybaord. 
* Research carefully and select the key switches you want. Switches.mx has great 
  information on different switches. For example, this is the info they have on the [Kalih BOX Navy](https://switches.mx/kailh-box-navy).
* Make sure to listen to key switches sound tests and look at the force-graphs to see the actuation
  points. This is especially important if you play games and want faster key presses.
* If you end up going with alps switches make sure to get the proper keycaps.
* If you want to save some money buy most of parts and materials on aliexpress but the 
  downside of purchasing the parts on aliexpress is the shipping time, usually over 30 days or longer.

### Tools 
<style>
.tablelines table, .tablelines td, .tablelines th {
        border: 1px solid black;
        }
</style>
| Tools              | Use Case        | URL     |
| -------------------|-----------------|---------|
| Glue Gun           | Glue things in place.|[link]()|
| Rosin Core solder  | Used for soldering.|[link]()|
| Small fan          | Stop fumes from going into your body.|[link]()|
| Soldering Station  | Soldering the metal contacts.|[link]()|
| Soldering Pencil   | Alternative tool for fine soldering.|[link](https://www.amazon.com/gp/product/B08B8L7C8D/ref=ox_sc_saved_title_2?smid=A1CJB5SYI9X4XC&psc=1)|
| Heat Insulation Mat| Used to organize tools and materials and prevent destruction of your table. |[link]()|
| Helping hands      | Extra hands are nice to have.|   [link]()|
| MX Switch opener   | If you want to lube your switches. | [link]()|
| Keycap remover     | Remove Keycaps safely and efficiently.| [link]()|
| Tweezers           | Great tool for tiny manuevers.|[link]()|
| wire cutter        | Cut wires.|[link]()|
| wire stripper      | Strip wires.|[link]()|

### Notes on Tools
* I would advice going to a maker studio to build the keyboard as they will have many of the tools I have listed above
but if you going to build more things in the future I would recommend investing in some of these tools.  

* Do not cheap out on the tools if you decide to build at home because you will end up wasting 
  your time which will make your build process painful and future projects a misery.

* For the soldering tool I would recommend the hakko station I linked above or better yet a Soldering pencil because of
  the somewhat small soldering pointpoints; a fine tip for the gun or pencil helps dramatically.

* Personally, I purchased a Hakko FX888D-23BY Digital Soldering Station and used my desoldering pump I purchased for my ECE class 
  and the keyboard build was somewhat easy overall.

## Build Guide Informations & Tips 

#### Intial 3D Printout
![Inital 3D Printout](https://raw.githubusercontent.com/morphykuffour/morphykuffour.github.io/main/images/dactyl_printout.jpg)  

### Wiring
* Follow [Nick Green's Build log](https://nickgreen.info/dactyl-manuform-build-log/) to build the keybaord. I like said in my
  intial motivation for this post. I wanted to create a supplement and point out caveats of the build process.
  * His wiring diagram was propably the most important guide for my build. See the image below.
  * ![wiring diagram](https://raw.githubusercontent.com/morphykuffour/morphykuffour.github.io/main/images/Wiring-Diagram-1.svg)  

* Follow [aaronmak's build guide ](https://arnmk.com/building-a-dactyl-manuform-with-hot-swappable-sockets/) to see how the
kalih hotswap sockets are setup.

* If you buy the cheaper, regular (non-hotswappable) case from Andrew on etsy.com which is what I recommend after completing my build.
but you decide you want a hostwappable keybaord then I would highly recommend the Amoeba Single-Switch PCBs as the PCB enables hotswappablenes. 

* The only annoying part of the single pcbs from keebio is that 1 order has 30 pcs and you need 64 pieces of the PCB for the dactyl build so you end spending extra for the extra 4 PCBs. 

* FYI, I purchased the hotswappable case from [Andrew on esty.com](https://www.etsy.com/listing/1028152282/made-to-order-dactyl-manuform).

* If you decide to use the PCB do not break them into individual parts before attaching the switches to the PCB, attach the switches first and then break them apart.  
  See this [reddit thread](https://www.reddit.com/r/olkb/comments/bajnlq/help_with_amoeba_single_switch_dactyl/) for more help on the amoeba PCB wiring setup with the dactyl manuform.

### Compiling code for custom QMK keymaps
If you are on windows follow the windows tab on from the follwing link in order to setup your build environment. [Setup QMK build Enivronment](https://docs.qmk.fm/#/getting_started_build_tools?id=set-up-your-environment)
I used 
Setup QMK and QMK toolbox on Macos

[Install Homebrew](https://brew.sh/)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
[Install qmk](https://qmk.fm/)
```bash
brew install qmk/qmk/qmk
```
Make sure to read the output from the installation of the qmk software installation. 
It will inform you if you need to install any additionaly dependencies neccessary for build and compiling your .hex file

[Install a proper editor ;) ](https://neovim.io/)
```bash
brew install neovim
```
Use the text editor to edit the keymaps and compile to create the .hex file.

### Flashing

[Install qmk toolbox](https://github.com/qmk/qmk_toolbox/releases)
The annoying thing on windows is that every time you connect the pro mirco 
by usb the os thinks it is being "smart" by automatically installing drivers for the pro micro
so you have to be physically fast clicking on flash in order to flash the hex file before windows recognizes the chip as a different device.

You do not have to install qmk toolbox if you don't want as qmk supports flashing the hex file you generate from the command line.
QMK toolbox is just easier and less error prone.

```bash
qmk compile -kb handwired/dactyl_manuform/6x6 -km custom;
qmk compile -kb handwired/dactyl_manuform/6x6 -km custom_right;
```
* These two commands will create 2 hex files and place them in **$QMK_HOME** directory.

* Use the QMK toolbox gui application to flash these hex files on the left and right pro micros.

* If you don't want to edit any code use [QMK's Online Configurator](https://config.qmk.fm/#/handwired/dactyl_manuform/5x6/LAYOUT_5x6) to create the hex files. 

[Personal QWERTY Keymap for Dactyl](https://github.com/morphykuffour/dactyl_manuform.git)
* ![my custom keympas](https://raw.githubusercontent.com/morphykuffour/morphykuffour.github.io/main/images/dactyl_manuform_keymaps.jpg)  

* Follow [balatero](https://balatero.com/writings/qmk/getting-started-with-dactyl-manuform-and-qmk/) to flash the QMK firmware on the pro micros. [David Balatero's Flashing Guide and Keymap setup](https://balatero.com/writings/qmk/getting-started-with-dactyl-manuform-and-qmk/)<br /> 

* Make sure that you connect both halves with the trrs cable before connecting the usb-c cable to your computer.

* Important flashing info provided by Nick Green: 

> Try loading the default hex as shown by the GUI, connect the left half to USB, with both halves connected together. Short the VCC and a GND port to put it in bootloader mode, and immediately hit **flash** in QMK Toolbox. Then, disconnect the left half and flash the right half the same way, with the same file. Then connect the left half again, and you should be getting letters when you type.


#### Final Setup 
![Final Setup with Gameball](https://raw.githubusercontent.com/morphykuffour/morphykuffour.github.io/main/images/dactyl_setup_croped.jpg)  

<!-- ## My C Further customizations going forward -->

## misc advice 
* Enable **EE_HANDS** in the rules.mk in the directory for the left half.

* Add a reset key known as **RESET** to a layer through the QMK firmware. This allows you to but the keyboard in flash mode using a key press on the actual keyboard.

* Use the jumper wires I linked above as the wires you connect to the pro mircos and pcb or the hot swaps or 
directly to the key switches if you decide to not go for a hotswappable build.

* If you decide to directly solder the switches make sure to get glue sticks the glue gun I linked above has plenty of glue included. 

* You will aslo want NKRO (N-Key Rollover) to prevent ghosting — letters missing from what you actually typed, 
or additional letters that you didn't type. 
NKRO should be naturally possible if you add a diode to each key switch. You will also want to enable NKRO in 
the keyboard's firmware by editing the rules.mk file in both of your custom folders.

* A regular aux cable will not work because it is a trs cable and you need a trrs cable in order to transmit data signals between the two pro micros.

* If you are building the dactyl manuform you have the option to use a RJ-9 female to female connection to connect the 
two halves. If I had to start over I would have gone with this approach because you don't have to remember to
always connect the two halves first before connecting to your computer.
 
## Mistakes I made
Getting the case printed without the Kalih Hot swap holders and buying the amoeba PCBs which I ended up not using. <br />
This would save some money. Also the plastic holders in the hotswap case 3D print by Andrew 
did not really hold the hot swaps in place well, they occasionally fell out.

## Helpful Links
[QMK Firmware Repo](https://github.com/qmk/qmk_firmware)<br />
[QMK Official Documentation](https://docs.qmk.fm/#/)<br />
[QMK Online Configurator](https://config.qmk.fm/)<br />
[Nick Green's Build log](https://nickgreen.info/dactyl-manuform-build-log/)<br />
[David Balatero's Flashing Guide and Keymap setup](https://balatero.com/writings/qmk/getting-started-with-dactyl-manuform-and-qmk/)<br /> 
<!-- [Install QMK on Windows]()<br /> --> 
<!-- [Install QMK on Mac OS]()<br /> --> 
<!-- https://switches.mx/kailh-box-navy?search=box& -->
