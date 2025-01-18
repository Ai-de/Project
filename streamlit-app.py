from crewai import Agent, Task, LLM, Crew
from crewai_tools import SerperDevTool
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

#Page config
st.set_page_config(page_title="Super Lit and Brainrot F1Tenth Poem", page_icon="YES SIRRR", layout="wide")

#Title
st.title("Super Lit and Brainrot Poem - Powered by the HUGOOO")
st.balloons()

#Sidebar
with st.sidebar:
    st.header("Content input")
    topic =st.text_area(
        "Enter your topic",
        height = 100,
        placeholder="Enter your topic"
    )

    st.markdown("## LLM Settings")
    temperature = st.slider("How deep?", 0.0, 1.0,0.7)

    st.markdown("--------")

    gen_button = st.button("Generate Content", type="primary")

    with st.expander("How do to use??"):
        st.markdown("""1. Enter your desired content topic\n
                   2. Select how deeeeeep.\n
                   3. Click Generate Content\n
                   4. Enjoy""")
        
def generate_content(topic):    
    llm = LLM(model = "gpt-4o-mini")

    #tool2
    search_tool = SerperDevTool(n=10)

    #Agent 1
    senior_research_analyst = Agent(
        role = "Senior Research Analyst",
        goal = f"Research, analyze and synthesis related information on {topic} from reliable sources",
        backstory = f"You are an experienced researchers who looks for related information"
                "about {topic}. Find information related to algorithms"
                ", related time and location, posts on the internet like Google and LinkedIn",
        allow_delegation = False,
        verbose = True,
            tools = [search_tool],
        llm = llm

    )

    #Agent 2 Content Writer
    content_writer = Agent (
        role = "Content Writer",
        goal = "tranform research findings into musically 4 words/ a line poet",
        backstory = f"You are a famous poem who likes to write about {topic}"
                "to convince people to like the topic. Make a very nice 10 lines, each line "
                "has 4 words. The poem should flow nicely and smoothly and attract people with the details",
        verbose = True,
        tools = [search_tool],
        llm = llm
    )

    #research task
    research_tasks = Task(
        description=("""
            1. Search on Google 
            2. Evaluate credibility 
            3. Organize findings in an easy to understand flow
            4. Find words with rhythm
        """),
        expected_output = f"Search online for all interesting information about the {topic}",
        agent = senior_research_analyst   
    
    )

    #Task 2 content writing
    poem_tasks = Task(
        description=("""
            1. Transform all content into step by step 
            2. Evaluate how fun it is
            3. Organize findings in 4 words on a line in the poem
            4. Find words with rhythm and refine the poem the final time
        """),
        expected_output = "A fun poem of 10 lines, with 4 words a line, talking about "
        f" the relate {topic}. End the poem with 1 word: cat",
        agent = content_writer  
    
    )

    crew = Crew(
        agents = [senior_research_analyst,content_writer],
        tasks = [research_tasks, poem_tasks],
        verbose = True
    )

    result = crew.kickoff(inputs= {"topic" : topic})
    return result

if gen_button:
    with st.spinner("Generating content... We are cooking hotpot cookin the hotpot"):
        try:
            result = generate_content(topic)
            st.markdown("### Generated Content")
            st.markdown(result)

            st.download_button(
                label = "Download Content",
                data = result.raw,
                file_name = f"{topic.lower().replace('','_')}_article.md",
                mime ="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occured: {str(e)}")

st.markdown("-----")
st.markdown("Built with Creq AI")