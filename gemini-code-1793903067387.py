import streamlit as st

# 1. 初始化遊戲狀態 (使用 session_state 儲存玩家進度與數值)
if 'current_scene' not in st.session_state:
    st.session_state.current_scene = 'scene_1'
    st.session_state.danger = 0
    st.session_state.trust = 50

# 2. 定義故事文本與選項 (對應你們企劃書中的 dict 與 json 格式概念)
storyline = {
    'scene_1': {
        'text': "1950年代的台灣大學校園。某天下午，你的一位平時很照顧你的學長把你拉到角落，神情緊張地問你：「我們最近在讀一些『不一樣』的書，你要不要也來參加我們的讀書會？」",
        'choices': [
            {'text': "答應參加", 'next_scene': 'scene_2_join', 'danger_change': 20, 'trust_change': 10},
            {'text': "委婉拒絕", 'next_scene': 'scene_2_reject', 'danger_change': 0, 'trust_change': -10},
        ]
    },
    'scene_2_join': {
        'text': "你加入了讀書會。你們在地下室閱讀馬克思的著作。突然，外面傳來急促的敲門聲和軍警的吆喝聲...",
        'choices': [
            {'text': "立刻將書本燒毀並從後門逃跑", 'next_scene': 'ending_escape', 'danger_change': 30, 'trust_change': 0},
            {'text': "保持冷靜，把書藏起來去應門", 'next_scene': 'ending_arrested', 'danger_change': 50, 'trust_change': 0}
        ]
    },
    'scene_2_reject': {
        'text': "你拒絕了學長。幾天後，你聽說學長失蹤了。今天學校裡出現了陌生的西裝男子在四處打聽他的下落，並向你走來...",
        'choices': [
            {'text': "裝作什麼都不知道", 'next_scene': 'ending_safe', 'danger_change': -10, 'trust_change': 0},
            {'text': "向他們透露學長之前的邀請", 'next_scene': 'ending_betrayal', 'danger_change': -20, 'trust_change': -50}
        ]
    },
    # 結局設計 (無後續選項)
    'ending_escape': {
        'text': "【結局：亡命天涯】你成功逃脫了逮捕，但從此只能隱姓埋名，過著躲躲藏藏的日子。你的危險值過高，雖然保住了性命，卻失去了原本的生活。",
        'choices': []
    },
    'ending_arrested': {
        'text': "【結局：鋃鐺入獄】軍警搜出了禁書，你被當場逮捕。在那個年代，等待你的將是漫長的審問與黑牢...",
        'choices': []
    },
    'ending_safe': {
        'text': "【結局：苟且偷生】你避開了嫌疑，但也永遠失去了那位學長。在戒嚴時期，明哲保身或許是唯一的生存法則，但你的良心始終受到煎熬。",
        'choices': []
    },
    'ending_betrayal': {
        'text': "【結局：背叛者】你出賣了學長換取自身的安全。你確實活了下來，但同學們看你的眼神再也不一樣了。在那個相互猜忌的年代，你成為了體制的幫兇。",
        'choices': []
    }
}

# 3. 定義處理選擇的函式
def make_choice(next_scene, danger_change, trust_change):
    st.session_state.current_scene = next_scene
    st.session_state.danger += danger_change
    st.session_state.trust += trust_change

# 4. UI 介面呈現
st.title("今日無事—臺灣白色恐怖互動式遊戲")
st.markdown("### Are You Really Safe?")

# 在側邊欄顯示玩家數值
st.sidebar.header("玩家狀態")
st.sidebar.write(f"⚠️ 危險值 (Danger): {st.session_state.danger}")
st.sidebar.write(f"🤝 信任值 (Trust): {st.session_state.trust}")
st.sidebar.markdown("---")
st.sidebar.info("不同的選擇將會影響你的危險值與他人的信任值，進而決定最後的結局。")

# 獲取當前場景資料
current_scene_data = storyline[st.session_state.current_scene]

# 顯示當前劇情文本
st.write(current_scene_data['text'])
st.write("---")

# 5. 生成選項按鈕 (對應 for loop 與 if/else 邏輯)
if current_scene_data['choices']:
    st.write("**請做出你的選擇：**")
    for idx, choice in enumerate(current_scene_data['choices']):
        st.button(
            choice['text'], 
            key=f"btn_{st.session_state.current_scene}_{idx}",
            on_click=make_choice,
            args=(choice['next_scene'], choice['danger_change'], choice['trust_change'])
        )
else:
    # 如果沒有選項，代表進入結局
    st.subheader("遊戲結束")
    if st.button("重新開始"):
        # 重置狀態
        st.session_state.current_scene = 'scene_1'
        st.session_state.danger = 0
        st.session_state.trust = 50
        st.rerun()