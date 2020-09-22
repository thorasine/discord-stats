import pandas as pd
import plotly
import plotly.graph_objs as go

person1 = "person1"
person2 = "Thorasine"
daily = False
messages = True

pd.set_option('display.expand_frame_repr', False)
fields = ['Author', 'Date', 'Content']
df = pd.read_csv('resources/' + person1 + '.csv', sep=',', usecols=fields)
df = df.dropna()
df['Author'] = df['Author'].map(lambda x: str(x)[:-5])

if daily:
    # daily
    df['Date'] = pd.to_datetime(df['Date']).dt.floor('D')
else:
    # monthly
    df['Date'] = df['Date'].map(lambda x: str(x)[:7])

if messages:
    # messages counter
    df = df.groupby(['Author', 'Date'])['Content'].count().reset_index(name="Count")
else:
    # words counter
    df['totalwords'] = [len(x.split()) for x in df['Content'].tolist()]
    df = df.groupby(['Author', 'Date'])['totalwords'].sum().reset_index(name="Count")

df1 = df[df.Author == person1][["Date", "Count"]]
df2 = df[df.Author == person2][["Date", "Count"]].reset_index(drop=True)
print(df1)
print(df2)

total1 = df[df.Author == person1][['Count']].sum()["Count"]
total2 = df[df.Author == person2][['Count']].sum()["Count"]
print("Total: " + str(total1 + total2))

trace1 = go.Bar(
    x=df1["Date"],
    y=df1["Count"],
    name=person1 + ": " + str(total1),
    text=df1["Count"],
    textposition='auto',
    marker=dict(
        color='rgb(117, 53, 109)'
    )
)
trace2 = go.Bar(
    x=df2["Date"],
    y=df2["Count"],
    name=person2 + ": " + str(total2),
    text=df2["Count"],
    textposition='auto',
    marker=dict(
        color='rgb(26, 118, 255)'
    )
)

data = [trace1, trace2]
layout = go.Layout(
    title=("Messages" if messages else "Words") + " sent " + ("daily " if daily else "monthly ") + "on Discord",
    xaxis=dict(
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        ),
        type='category',
    ),
    yaxis=dict(
        title=("Messages" if messages else "Words" + " sent"),
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    legend=dict(
        x=0.0,
        y=1.1,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.2,
    bargroupgap=0.0
)

fig = go.Figure(data=data, layout=layout)
name = "html/" + person1 + (" messages" if messages else " words") + (" daily" if daily else " monthly") + ".html"
plotly.offline.plot(fig, filename=name)
fig.write_image("images/" + name[5:-5] + ".png",  width=2000, height=1000, scale=1.0)