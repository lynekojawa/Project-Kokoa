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

