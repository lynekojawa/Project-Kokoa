(9/23)
Set up the project repo for new project. Second attempt for the local LLM.

(9/24)
Continue the project, start with phase 0. 
Constraints and rules are cleared. You have:

$$T_{\text{planned}} \approx T_{\text{reps}} + T_{\text{rest}}$$

But T_rest isn't defined in the formula. It should be:

$$T_{\text{planned}} \approx (N_{\text{sets}} \times T_{\text{rep\_duration}}) + ((N_{\text{sets}} - 1) \times T_{\text{rest}}) + T_{\text{transition}}$$
need to watch out for this but otherwise ready for the SQL schema. 
Certainly GPT Orion is quite intersting he makes plans for three-four rounds then finally make one which I appreciate, but 
I wouldn't recommend newbie for GPT there are lots of things to concern before you even proceed and easy to lost. 
Defined folder structure, tomorrow phase 1 implementation start with SQL schema. 

(9/28)
Continue project.

PYTHONPATH=. pytest tests/persistence/test_database.py -v 
it doesn't run the test unless I give it full path. is there
anyway I can do without telling it? YES
Created toml file and put [tool.pytest.ini_options]
pythonpath = ["."] and now it works without whole path command! :D 

Created: database.py, test_database.py, runner.py, test_migration_runner.py

(9/29)
Continue project.
Start it from test_migration_runner.py
So far the combination of GPT Orion and mini-Dante Cluade and little cheer Podo is pretty good. what I am worrying about<br>
is how is the final result will looks like, I think in my sense it has detailed structure and I haven't faced hallucinations
but is also feels like very detail from file to file(which I appreciate), and I will record it again once the UI comes out
I hope this isn't turning into another project Q, dealing with local LLM is harder than it looks like, and is it worth? 
I think it is for the many reasons but creating an environment for LLM is bit much. 

Edited: runner.py -> Removed redundant, Gap detection
test_migration_runner.py -> add gap in migration test, passing all 5 tests. 
Created: 001_initial_schema.py, 

(9/30)
Continue project. 
I feel like recent UI's are very small and the ratio too. Especially when it comes to the code space that is given... 
I noticed it's been 2 weeks since I canceled my gemini-pro, and I think that was best choice. Gemini-forget things too quickly
They are good for simple working and fast working, but not at deep work. 

I think it's very interesting """ """ also used for the comments while it can also be a command for the sqlite. 


Edited: 001_initial_schema-> typos, commas, all the little things. registry.py-> add comments
Created: registry.py, test_initial_schema.py
Next session: Encapsulation in Database class. 