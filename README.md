# Student Number Checksum Calculation

Each student at a certain institution is assigned an id of format SXXXXXXXXY, where X can be a number from 0-9 and Y an alphabet in ABCDEFGHJK. One can assume that the last alphabet is probably a checkdigit, which can be calculated from the previous numbers to verify that the information entered is correct. With no documentation to be found anywhere, I decided to try and figure out how the checksum is calculated.

The first checksum scheme that comes to mind (and the only one I've played with at this point) is the one used in the Singapore NRIC. [A description of how it is calculated can be found here](http://coding-and-crypto.tripod.com/01NRIC.htm)

Each number in the NRIC is multiplied by a weight unique to each position, then summed together. The modulo (remainder) 11 of the sum then points to a corresponding check digit.

To apply this method to the student ids, we need a few more pieces of information. What is the modulo number to use? What are the weights to multiply by?

### Modulo Number
Through simple data processing with a large list of student ids, I identified that there were 10 possible check digits, ABCDEFGHJK. This points to a modulo number of 10 (if the modulo checksum scheme is even used)

### Weights
To calculate the weights, I chose the simplest, most inefficient method: bruteforce. For every possible value of weights [11111111, 99999999], its correctness can be validated by using it to calculate the check digits of a list of student ids. The check digit calculated with my weights can then be compared to the original, correct check digit. If all of them match, the weights are correct.

A quick python script was whipped up to implement the above (bruteforce.py). To speed up the bruteforce and make full use of the resources available to me, 4 workers were ran across the 4 CPU cores on my machine with each worker focusing on a different segment of [11111111, 99999999].

Much to my surprise - the script spat out 10 possible weights, all of which passed the test. These are 70379139, 71379139, 72379139 ... 79379139. These all differ only in the second weight. This can be explained with the range of student ids available for calculation as all the student ids I used above started with either S100 or S101. The second place was 0 in all student ids I had available, hence whether the weight for 0 was 1, 5, 8, or 9, it played no part in the check digit calculation.

Having tested with over 2000 student ids, I can only assume that these weights are correct.

### Application
A javascript based calculator has been implemented in stdno_checksum.html for easy use. Being able to validate the correctness of student ids comes in very handy when collecting information from other students. When they inevitably fat-finger their student id, I can go back and reconfirm their student id with them. This makes matching records in spreadsheets far simpler when using student ids as unique keys.