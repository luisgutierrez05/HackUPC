import streamlit as st
import pandas as pd
import numpy as np
import requests
import random
from PIL import Image
import requests
from urllib.request import urlopen
from io import BytesIO
        
# Basic configuration of the webpage
st.set_page_config(
    page_title="Inditextech Challenge",
    initial_sidebar_state="expanded",
    layout="centered"
)

# Title of the page and some text
st.title("Inditextech Challenge!")

st.sidebar.markdown("# Home 🎈")

st.info("Welcome to our project! ⛩️", icon="⛩️")

st.write(" ")
st.write("---")
st.write(" ")

st.subheader("About Us")

# Team members info
team_members = [
    {
        "name": "Jan Matas",
        "degree": "Computer Engineering",
        "linkedin": "https://www.linkedin.com/in/jan-matas-cantos-049361286/",
    },
    {
        "name": "Bernat Pages",
        "degree": "Mathematics and Data Science and Engineering",
        "linkedin": "https://www.linkedin.com/in/bernat-pag%C3%A8s-vives/",
    },
    {
        "name": "Luis Gutierrez",
        "degree": "Mathematics and Physics Engineering",
        "linkedin": "https://www.linkedin.com/in/luis-guti%C3%A9rrez-garrido-2a7459284/",
    },
    {
        "name": "Joan Pascual",
        "degree": "Mathematics and Physics Engineering",
        "linkedin": "https://www.linkedin.com/in/joan-pascual-ribes-7a974b284/",
    }
]

# Set up columns for horizontal layout
col1, col2 = st.columns(2)
cols = [col1, col2, col1, col2]

# Show the members info
for member, col in list(zip(team_members, cols)):
    with col:
        c = st.container()
        c.write(f"### {member['name']}")
        c.markdown(f"<u>Degrees</u>: {member['degree']}", unsafe_allow_html=True)
        c.write(f"Linkedin: [{member['name']}]({member['linkedin']})")


st.write(" ")
st.write("---")
st.write(" ")


# 
# This part consists on testing our model and showing results
#

st.write("## Testing Our Model")

# Get the dataframe
PATH = 'data/'
df = pd.read_csv(PATH + 'raw_data.csv')

# Number of rows and columns from the dataframe
ROWS = df.shape[0]
COLS = df.shape[1]

# \pre The url is valid
# \post Returns the image of the url
def get_image(url):
    #data = requests.get(url).content
    #img = Image.open(BytesIO(data))
    img = Image.open(urlopen(url))
    return img

# \pre x is a 3d np array where x[i][j] is the vector of values of each color (RGB) 
# from the pixel in position (i, j) 
# \post The histogram is computed
def compute_histogram(x):
    # We divide the scalars of the histogram in 16 categories where each one englobes 16 levels of color
    rgb_histogram = [[[0 for i in range(16)] for j in range(16)] for k in range(16)]
    for i in range(len(x)):
        for j in range(len(x[0])):
            # Add the pixel in the appropiate positions
            rgb_histogram[x[i][j][0] // 16][x[i][j][1] // 16][x[i][j][2] // 16] += 1
    return rgb_histogram

# \pre x and y are 3d np arrays 
# \post The difference betweeen two histograms is computed using efficient formulas
def dist2(x, y):
    max_x = 0
    max_y = 0
    for i in x: 
        for j in i:
            for k in j: 
                max_x = max(max_x,k)
    for i in y: 
        for j in i: 
            for k in j:
                max_y = max(max_y,k)
    cnt = 0.0
    for i in range(len(x)):
        for j in range(len(x[0])):
            for k in range(len(x[0][0])):
                if x[i][j][k] != max_x and y[i][j][k] != max_y:
                    cnt += abs((x[i][j][k] + 1) - (y[i][j][k] + 1))
    return cnt

NUMBER_SUBSET = 100
NUMBER_CANDIDATES = 4

# \pre The url is valid
# \post The matrix of the image of the url is returned
def get_matrix(url):
    x = np.array(get_image(url).resize((128, 128)))
    return x

# Get the urls of all images
urls = pd.read_csv("data/raw_data.csv")

# List where we store the info of every pixel of the images
data = []

# \pre end <= number of the last image
# \post The data is stored in data
def get_batch(start, end):
    for i in range(start, min(end, urls.shape[0])):
        for j in range(urls.iloc[i].shape[0]):
            try:
                #array_data = np.load(f'data/proc_data/{i//100}/{i}_{j}.npy')
                array_data = np.load(f'data/archivos/{i // 100}/{i}_{j}.npy')
                
                data.append([array_data, i, j])

            except:
                continue
        
get_batch(0,1000)

# \pre The url is valid
# \post A list with the top NUMBER_CANDIDATE image's that are most similar with the image specified in url
def solve(url,i1,j1):
    # Get matrix from the image we want
    x = get_matrix(url)
                
    candidates = []


    x_hist = compute_histogram(x)

    try:
        y = get_matrix(df.iloc[i1, 0])
        candidates.append([dist2(x_hist, compute_histogram(y)), df.iloc[i1, 0]])
    except:
        pass
    try:
        y = get_matrix(df.iloc[i1, 1])
        candidates.append([dist2(x_hist, compute_histogram(y)), df.iloc[i1, 1]])
    except:
        pass
    try:
        y = get_matrix(df.iloc[i1, 2])
        candidates.append([dist2(x_hist, compute_histogram(y)), df.iloc[i1, 2]])
    except:
     pass


    # Get K candidates 
    for _ in range(NUMBER_SUBSET):
        # Get random indexes and the url in that position
        rand = random.randint(0, len(data) - 1)
        newhist =  compute_histogram(data[rand][0])
        # Add the difference between the histograms
        candidates.append([dist2(x_hist, newhist), df.iloc[data[rand][1], data[rand][2]]])
    
    # Sort the array
    candidates.sort()

    # Get the best candidates 
    ans = []
    for i in range(NUMBER_CANDIDATES):
        ans.append(candidates[i][1])
    return ans

# \pre True
# \post Get random url 
def get_random_url():
    i = np.random.randint(0, ROWS - 1)
    j = np.random.randint(0, COLS - 1)
    url = df.iloc[i, j]
    return url,i,j

# \pre The url is valid
# \post The image from the url is shown in the app
def show_image(url):
    st.image(url, use_column_width=True)
    #request = requests.get(url)
    #img = Image.open(BytesIO(request.content))

st.write(" ")

# Button to generate image and similarities
if st.button('Generate Image and Similars'):
    # Get url and show it
    url,i1,j1 = get_random_url()
    show_image(url)

    # Get the url's from 
    links = solve(url,i1,j1)

    # Divide row into rows
    cols = st.columns(NUMBER_CANDIDATES)

    # Print the most similars images
    i = 0
    for col in cols:
        with col:
            st.image(links[i], use_column_width=True)
        i += 1

    

