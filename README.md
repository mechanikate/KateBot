<div align="center">
    <img src="logo.png" height=64 alt="KateBot logo" />
    <hr />
</div>
Hello! This is my Python-based Discord bot.

<h1>Commands</h1>
App commands for KateBot.

<h2>Economy</h2>
<i>Category.</i>

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

<h2>Fun</h2>
<i>Category.</i>

<h4><code>/consulify (message) [as_emojis]</code></h4>
Turns string <code>message</code> into Xenoblade Chronicles' Consuls as emojis by default (with <code>as_emojis = true</code>). Also can be requested into raw text via setting <code>as_emojis = false</code>.
Spaces in <code>message</code> result in new lines.

<br /><br />
<i>Example output.</i>
<code>/consulify message: Hello as_emojis: false</code> &rarr; <code>:Hh: :Ee: :Ll: :Ll: :Oo:</code>

<h4><code>/kateban (user)</code></h4>
"Bans" user <code>user</code>. The user is not banned in actuality, the command just sends a success message saying that user <code>user</code> was banned.
Some users cannot be fake banned, including KateBot itself, the bot's owner, and other configurable users. In these cases, the bot will respond with hostility.
<br /><br />
<i>Example output.</i>
<code>/kateban user: @example_user reason: test</code> &rarr; <code>✅: @example_user has been banned for reason: test</code>

<h4><code>/wisdom</code></h4>
Gives 1 piece of wisdom from bot developer mechanikate, configurable in <code>cogs/fun_commands.py</code>'s <code>wisdom_list</code> constant. Runnable once per hour per guild.
<br /><br />
<i>Example output.</i>
<code>/wisdom</code> &rarr; <code>8. Nobody knows how the water got in the coconut. It's a fact of life.</code>

<h4><code>/coinflip</code></h4>
Flips a coin. 
<br /><br />
<i>Example output.</i>
<code>/coinflip</code> &rarr; <code>It's tails! Now at 43/85 (50.588235294117645%) tails.</code>

