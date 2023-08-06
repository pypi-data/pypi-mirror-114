# Installation

Clone this repository and run

`pip install --user git+https://github.com/sigmind-org/sigmind_tools`

**Important!** Store your aws credentials to call the services in 

`~/.aws/credentials`

# Functions
## Audio functions
All functions that receive an audio file has three disjoint ways to get the audio. Regarding the audio format,  the functions support almost any format.

1. Parameters for public url audio method:
    - url: An public url with a audio
2. Parameters for S3 audio method:
    - bucket (string): the name of the bucket
    - key (string): object key      
    Note: The bucket and object have to be accesble by the lambda function
3. Parameters for file method:
    - fn (string): local file name 
    
    
### Speech to text 
This use the Google Speech to text to transcript audio file. 
It supports almost every audio file format as input. 
    
This function need *language_code* as an extra paramter.


```python
from sigmind_tools import SigmindTools
st = SigmindTools()

# call with public audio url
st.speech_to_text(url=<PUBLIC_URL_OF_AUDIO_FILE>, language_code='en-US')

# call example with s3
st.speech_to_text(bucket=<BUCKET_NAME>,key=<OBJECT_KEY>, language_code='en-US')

# call example with local file
st.speech_to_text(fn=<LOCAL_FILENAME>, language_code='en-US')

```
 
It returns (every function call)

```json
{
   "timeline_activity":{
      "transcript":"Hola c\u00f3mo",
      "confidence":0.9256038665771484,
      "times":[
         {
            "word":"Hola",
            "start_time":0,
            "end_time":1100
         },
         {
            "word":"c\u00f3mo",
            "start_time":1100,
            "end_time":2600
         }
      ],
      "duration":2600
   },
   "query_timestamp_start":"2021-03-22 22:08:55.979719",
   "query_duration":6.351794
}
```


### Speech intervals  
This method computes the interval with active speech 

```python

# call with public audio url
st.speech_intervals(url=<PUBLIC_URL_OF_AUDIO_FILE>)

# call example with s3
st.speech_intervals(bucket=<BUCKET_NAME>,key=<OBJECT_KEY>)

# call example with local file
st.speech_intervals(fn=<LOCAL_FILENAME>)
```

It returns

```json
{
   "timeline_activity":[
      [
         0.8437812499999999,
         1.2200937499999998
      ],
      [
         2.25115625,
         2.8147812500000002
      ],
      [
         5.4658437499999994,
         6.14759375
      ]
   ],
   "query_timestamp_start":"2021-03-22 22:07:57.886976",
   "query_duration":1.200753
}
```

### Pitch analysis

```python
# call with public audio url
st.pitch_analysis(url=<PUBLIC_URL_OF_AUDIO_FILE>)

# call example with s3
st.pitch_analysis(bucket=<BUCKET_NAME>,key=<OBJECT_KEY>)

# call example with local file
st.pitch_analysis(fn=<LOCAL_FILENAME>)
```

It returns

```json
{
   "pitch_series":[
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      30.054454803466797,
      29.85991096496582,
      
      ...
      
      28.461585998535156,
      28.81536102294922,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      32.78231430053711,
      32.21982192993164,
      31.312158584594727,
      0.0,
      0.0,
      0.0,
   ],
   "sample_hz":"100",
   "query_timestamp_start":"2021-03-31 14:02:06.447588",
   "query_duration":1.399988
}
```

## Text functions
  
### Sentiment Analysis

```python
from sigmind_tools import SigmindTools
st = SigmindTools()

text = """La salud mental abarca una amplia gama de actividades directa
 o indirectamente relacionadas con el componente de bienestar mental 
 incluido en la definición de salud que da la OMS: «un estado de completo 
 bienestar físico, mental y social, y no solamente la ausencia de afecciones
  o enfermedades"""

st.sentiment_analysis(text)
```

it returns

```json
{
   "score":0.20000000298023224,
   "magnitude":0.20000000298023224,
   "lang":"es",
   "query_timestamp_start":"2021-03-31 14:08:09.555727",
   "query_duration":1.141135
}
```


### Text Indexes
```python
st = SigmindTools()
st.text_indexes(text)
```

it returns

```json
{
   "flesch_reading_ease":-1.62,
   "smog_index":0.0,
   "flesch_kincaid_grade":25.2,
   "coleman_liau_index":14.23,
   "automated_readability_index":27.2,
   "dale_chall_readability_score":12.35,
   "difficult_words":19,
   "linsear_write_formula":34.5,
   "gunning_fog":27.31,
   "text_standard":"12th and 13th grade",
   "fernandez_huerta":44.9,
   "szigriszt_pazos":43.19,
   "gutierrez_polini":27.57,
   "crawford":5.3,
   "query_timestamp_start":"2021-03-31 14:10:01.680797",
   "query_duration":2.507043
}
```
