<div align="center">
    <img src="logo.png" height=64 alt="KateBot logo" />
    <hr />
</div>
Hello! This is my Python-based Discord bot.

<h1>Commands</h1>
App commands for KateBot.

<h2>Economy</h2>

<h4><code>/balance [user]</code></h4>
View the balance of a specific person. 

<code>user</code> defaults to the command runner.
<br /><br />
<i>Example output.</i> <code>/balance user:@mechanikate</code> &rarr; <code>mechanikate has $204.35.</code>

<h4><code>/leaderboard</code></h4>
View the most rich people in the server.

<h4><code>/blackjack [wager]</code></h4>
Gambles <code>wager</code> dollar(s) (defaulting to $1.00) via a game of blackjack.

<h4><code>/gamble</code></h4>
Gambles 1 dollar with winners being decided by a super-secret algorithm.
<br /><br />
<i>Example output.</i> <code>/gamble</code> &rarr; <code>You win $3.48!</code>

<i>Example output.</i> <code>/gamble</code> &rarr; <code>You lost $1.00 :(</code>

<h3><code>/adminbalances</code></h3>
<i>Command group.</i>

<h4><code>/adminbalances set (new_balance) [target_user]</code></h4>
Set the balance of the user <code>target_user</code> to <code>new_balance</code> dollars.

<code>target_user</code> defaults to the command runner.
<br /><br />
<i>Example output.</i> 
<code>/adminbalances set new_balance: 204.35 target_user: @mechanikate</code> &rarr; <code>Set balance of mechanikate to $204.35.</code>

<h4><code>/adminbalances give (amount) [target_user]</code></h4>
Gives the user <code>target_user</code> <code>amount</code> more dollars.

<code>target_user</code> defaults to the command runner.
<br /><br />
<i>Example output.</i> 
<code>/adminbalances give amount: 1 target_user: @mechanikate</code> &rarr; <code>Set balance of mechanikate from $204.35 to $205.35.</code>

<h4><code>/adminbalances remove (amount) [target_user]</code></h4>
Takes <code>amount</code> dollars from user <code>target_user</code>.

<code>target_user</code> defaults to the command runner.
<br /><br />
<i>Example output.</i> 
<code>/adminbalances remove amount: 1 target_user: @mechanikate</code> &rarr; <code>Set balance of mechanikate from $205.35 to $204.35.</code>

<h3><code>/adminpayouts</code></h3>
<i>Command group.</i>

<h4><code>/adminpayouts win (multiplier)</code></h4>
Sets the payout multiplier for winning blackjack (but not hitting 21, see <code>/adminpayouts blackjack</code>) to <code>multiplier</code> times your payout.
<br /><br />
<i>Example output.</i>
<code>/adminpayouts win multiplier:2</code> &rarr; <code>Set win multiplier from 1.5x to 2.0x.</code>

<h4><code>/adminpayouts blackjack (multiplier)</code></h4>
Sets the payout multiplier for hitting blackjack (21) in blackjack to <code>multiplier</code> times your payout.
<br /><br />
<i>Example output.</i>
<code>/adminpayouts blackjack multiplier:3</code> &rarr; <code>Set blackjack multiplier from 2x to 3.0x.</code>

<h4><code>/adminpayouts forfeit (multiplier)</code></h4>
Sets the payout multiplier for forfeiting in blackjack to <code>multiplier</code> times your payout.
<br /><br />
<i>Example output.</i>
<code>/adminpayouts forfeit multiplier:0.25</code> &rarr; <code>Set blackjack multiplier from 0.5x to 0.25x.</code>
