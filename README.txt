Eli Schwamm
Travers Parsons-Grayson
Deep Learning Final Project

_____________________   _____  ________    _______  ___________
\______   \_   _____/  /  _  \ \______ \   \      \ \_   _____/
 |       _/|    __)_  /  /_\  \ |    |  \  /   |   \ |    __)_ 
 |    |   \|        \/    |    \|    `   \/    |    \|        \
 |____|_  /_______  /\____|__  /_______  /\____|__  /_______  /
        \/        \/         \/        \/         \/        \/

############################    Section 1: Introduction         ##########################

Some of the widest reaching AI work has been the development of machines that beat humans at our favorite games. Beginning with IBM’s Deep Blue in the late 1990’s (which was constructed with a substantially different architecture than are neural networks, to the point where some question whether it was machine learning at all), moving to Google’s AlphaGo and AlphaGo Zero, and most recently, to openAI’s DOTA 2 network, machines that beat top ranked players at popular games captivate the public. Maybe the head-to-head nature of these games appeals to the our fantasies of the immanent approach of the singularity. I think there is a strong case to be made that AI research has targeted games because of this appeal, and because they are ideal tasks for neural networks. Most “games of wit,” such as chess and Go, are actually games of pattern recognition. In the clearly defined boundaries of a game, where the number of variables and outcomes are finite, talent is determined in large part by the amount of data processed and retained. Neural networks are able to process and retain in minutes what humans can process in years. 

Notably absent from the newspapers and tech blogs are any neural networks that have mastered poker. Perhaps this is because of how much poker relies on player behavior, scouring opponents faces for tells while masking one’s own. We set out to answer the question of how much about a poker game can be learned by studying only player behavior. Of course we do not have the capacity to scan players’ faces for tells (though in a not too distant future this will be possible. The ethics of it are another question.), so instead we settled for examining player bet behavior. To accomplish this, we downloaded a dump of more than 100,000 hands from a poker hand aggregating service, hhsmithy (www.hhsmithy.com) which downloads hands daily from the popular online poker sites IPoker, 888, PartyPokerNJ, Winamax, and WinningPoker. Unfortunately, hand files were saved in a plaintext format that stepped through the game in a line-by-line fashion. Below is an example of one game. 

	Stage #3017235114: Holdem  No Limit $0.50 - 2009-07-01 00:00:01 (ET)
	Table: DEFIANCE ST (Real Money) Seat #6 is the dealer
	Seat 6 - C71mm6MhFIxjPW1vaAXL1g ($55.30 in chips)
	Seat 2 - Qt5Yyd/Y121jtIk37c7TSg ($12.82 in chips)
	Seat 3 - l1bCLGuFqeFRwUfPsiDu/g ($147.69 in chips)
	Seat 4 - 13/ez0NPA4uRcBJ1Rafl6A ($17.90 in chips)
	Seat 5 - TmKBFDTMzV3f+C/n1iWjGQ ($46.04 in chips)
	Qt5Yyd/Y121jtIk37c7TSg - Posts small blind $0.25
	l1bCLGuFqeFRwUfPsiDu/g - Posts big blind $0.50
	*** POCKET CARDS ***
	13/ez0NPA4uRcBJ1Rafl6A - Folds
	TmKBFDTMzV3f+C/n1iWjGQ - Folds
	C71mm6MhFIxjPW1vaAXL1g - Folds
	Qt5Yyd/Y121jtIk37c7TSg - Folds
	*** SHOW DOWN ***
	l1bCLGuFqeFRwUfPsiDu/g - Does not show
	l1bCLGuFqeFRwUfPsiDu/g Collects $0.75 from main pot
	*** SUMMARY ***
	Total Pot($0.75)
	Seat 2: Qt5Yyd/Y121jtIk37c7TSg (small blind) Folded on the POCKET CARDS
	Seat 3: l1bCLGuFqeFRwUfPsiDu/g (big blind) collected Total ($0.75)
	Seat 4: 13/ez0NPA4uRcBJ1Rafl6A Folded on the POCKET CARDS
	Seat 5: TmKBFDTMzV3f+C/n1iWjGQ Folded on the POCKET CARDS
	Seat 6: C71mm6MhFIxjPW1vaAXL1g (dealer) Folded on the POCKET CARDS


#########################    Section 2: The Parser       #################################

The first step was to convert these text files into a .csv format where each row corresponds to a game and each column corresponds to information about the game we wish to capture. The full commented code of our parser (parser.py) is included in this directory, but the basic idea is as follows. The parser takes in each line of the file as a separate string, and updates a series of variables and indices accordingly. The most important of these variables is the gameState, which represents where in the process of the game the text is situated, and is updated when certain keywords are encountered. For example, any time the text “*** POCKET CARDS ***” is encountered, the gameState is switched to 3. Based on the gameState, then, values are searched for, extracted, and packaged in arrays. In gameState 3, for example, the term “raise” triggers a function that adds the dollar amount of the raise to the potSize variable and to the array for raises in the pocket cards gameState. Finally, at the end of each game, the parser saves these arrays as one row in a .csv, and subsequently resets them all to their starting values. The final output of the parser is a .csv file containing for each of the 6 players (in order of dealer first, right of the dealer second, etc) obfuscated name (player identifier, e.g. C71mm6MhFIxjPW1vaAXL1g), stack size (amount of money in chips e.g. $55.30), average ratio bet, raise, and call size to pot size during the pocket cards phase for each player (e.g. $0), the same ratio during the flop, turn, and river phases, and finally the winner of the game. Note, bet sizes were captured as a fraction of the total pot size because this is typically how a bet size is measured in poker community. To run the parser, simply place it in the same folder as the data files and execute it via python. The plaintext data files are too large to include in the repository, but below is a link to their source

http://web.archive.org/web/20110205042259/http://www.outflopped.com/questions/286/obfuscated-datamined-hand-histories

######################    Section 3: Further Data Cleaning       #########################

After the parser completed its run, the resulting .csv needs some additional cleaning before it can be taken as an input into the Keras model. Keras is an extension written for python that allows simple programming of neural networks. It relies on google’s tensorflow neural network platform for computation. To work with this data in Keras, we chose to remove games in which more than one individual wins (we treat winner as a categorical variable because in all games except ~1,000 only 1 individual wins. If we were to instead treat winning as a series of 6 binary variables, which could each independently take on values 0 (losing) or 1 (winning), than the network could achieve an accuracy of about 83% just by guessing that ever player loses every game). The data cleaning file, data_cleaning.R (written in R because of the convenience of the dpylr package for such tasks) is included in this repository. For convenience, the cleaned data file, poker_data_clean.csv is also included. 

######################    Section 4: Constructing the Network    #########################

Due to the simplicity of the inputed data structure, the neural network structure was similarly straightforward. It is a sequential network that consists of 5 layers, with 72, 108, 40, 16, and 6 nodes respectively. Fundamentally, neural networks work by passing information (in this case a number) between receptacles called “nodes” through pathways called “edges”. The first layer (set of nodes) is is all of the columns in our .csv. The final layer, is the network’s prediction about who won the poker game (This prediction can be either categorical, of the type “player 5 won,” or a vector of probabilities that each player won the game. The latter is vastly more efficient for training the network). As information passes through and edge, it is affected by the “edge weight.” Physiologically, this is analogous to the sensitivity of the synapse between two neurons. Philosophically, edge weight is a measure of the magnitude of the relationship between the node before and the node after the edge. Mathematically, the edge weight is a scalar which is multiplied by the value being passed through it. Once a node receives information from all of the edges entering it (inputs), it applies an “activation function.” This is to rescale the data this node passes though the edges leaving it (outputs) so as to avoid certain undesirable values. In our case, apply a ReLU or Rectified Linear Unit activation function. The ReLu has the form max(0,X), meaning if the value of the weighted sum of inputs to the node are negative, the node takes on the value 0. Otherwise, the node’s value is the sum of the values of the weighted sum of its inputs. This is analogous physiologically to the “threshold effect” for the firing of a neuron. When X>0, the magnitude of the node can be thought of as the rate of firing of a neuron. The final set of nodes has the “softmax” activation function, which is ideal for outputs that represent probabilities. The last technical note about our network is that it uses the “categorical crossentropy” loss function. When the neural network trains, it needs to have a way of measuring how successful it is at predicting poker outcomes. Further, it needs to be able to “backpropegate,” measure how much each of the edges contributed to the total error in the output of the network. Categorical crossentropy is a loss function designed for predicting categorical outcomes, such as the winner of a poker game. We trained our network for 200 epochs (rounds or error calculation and edge weight adjustment). 

######################    Section 5: Results    ########################################

### -----------------------------------------------------------------------------------###

ALL 72 VARIABLES - We first trained our model using an arbitary subset of 17,000 games (rows) from our dataset. We used all 72 input variables. 

17000/17000 [==============================] - 2s 106us/step - loss: 0.4658 - acc: 0.8604

ACCURACY: 84.44%

After 200 epochs the accuracy of our model was ~0.86 for the training set. After training the model, we tested the model on a different subset of 17,000 games. The model had an accuracy of 84.4%. 

------------------
WITHOUT STACK SIZE
------------------

ACCURACY: --> | | 88.71% | | <--
NOTE: The accuracy is increased when the stack size is removed likely because the stack size provides little to no useful information about who is going to win the game. We originally thought that this might be a proxy variable for how often a player wins, but if that is the case, our model is not recognizing it. Basically, then, the stack size variables serve only to increase the amount of epochs the model takes to train, as it has to shrink weights for the edges that carry stack size information. If we had the computational power to run models to a state of better convergence, we would expect this difference to disappear. 
 
### -----------------------------------------------------------------------------------###

FIRST 12 VARIABLES -  Next we trained our model instead using the first 12 variables as input variables. The first 6 variables represent the stack size of the 6 players, and the next 6 variables represent the amount bet by each player relative to the size of the pot in the *** POCKET CARDS *** stage. We used the same set-up as beforem training our model with 17,000 games.

17000/17000 [==============================] - 2s 91us/step - loss: 1.1299 - acc: 0.7037

ACCURACY: 70.24%

After 200 epochs the accuracy of our model was ~0.70 for the training set. Once again after training the model, we tested the model on a different subset of 17,000 games. The model had an accuracy of 70.24%. 

------------------
WITHOUT STACK SIZE
------------------

ACCURACY: 72.04%

### -----------------------------------------------------------------------------------###

FIRST 24 VARIABLES - The model was trained with 24 input variables. Once again the stack sizes, and bet size in *** POCKET CARDS ***. Additionally we now have information of the "calls" of players in *** POCKET CARDS *** and the bets in 
*** FLOP ***. 

17000/17000 [==============================] - 2s 97us/step - loss: 0.8455 - acc: 0.7225

ACCURACY: 72.36%

After 200 epochs the accuracy of our model was ~0.72 for the training set. Once again after training the model, we tested the model on a different subset of 17,000 games. The model had an accuracy of 72.36%. 

------------------
WITHOUT STACK SIZE
------------------

ACCURACY: 75.90%

### -----------------------------------------------------------------------------------###

######################    Section 6: Conclusion    #######################################

This project represents a foray into capturing the relationship between player betting behavior and winning in poker. In general, we found that with information on all bets, calls, and raises, the neural network was able to predict the winner of a game with incredible accuracy. This is not altogether surprising, though, as a player who is still betting and raising late in the game is extremely likely to win. However, even when we restricted the network’s inputs to player actions during the pocket cards and the flop, we found that approximately 75% of all match winners can be predicted from betting behavior during the early game alone. This means that 75% of the information needed to know who will win a hand is available to all players at the table. The skill and challenge in poker, then, is to ascertain as much of the remaining 25% as possible through other means. It is important to note that our sample of online poker is not representative for all poker, especially considering that the general low stakes and impersonal atmosphere of the web encourages tighter more algorithmic play. 

######################    Section 6: How to Use    #######################################
1. cd into the directory with final.py, flopBet.py ...
2. For your file of choice type in the console <python filename.py> and press enter
   - The neural network will be run using the file with the chosen inputs

