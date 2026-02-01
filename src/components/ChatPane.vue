<script setup lang="ts">
import { onMounted, ref, nextTick } from 'vue';
import BotResponse from './BotResponse.vue';

import { postToBackend, handleBackendResponse } from '../services/backendComms'

import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();

import type { AxiosResponse } from 'axios';

const loading = ref<boolean>(false);

type Message = {
    text: string;
    type: 'user' | 'bot' | string;
    idx?: number;
    last?: boolean;
    link?: string | null;
    src?: string | null;
    audioSrc?: string | null;
    options?: { title: string; text: string; }[] | null;
    backendData?: any;
};

const chatMessages = ref<Message[]>([]);
const chatInput = ref<string>("");

const historyPane = ref<HTMLElement | null>(null);

let autoBot = true;

const emit = defineEmits<{
    (e: 'message', message: { text: string; type: string }): void;
    (e: 'showImage', src: string, more?: string): void;
    (e: 'showFrame', src: string, more?: string): void;
    (e: 'playAudio', src: string, more?: string): void;
    (e: 'clear'): void;
}>();



const scrollHistoryToBottom = async () => {
    await nextTick();
    const el = historyPane.value;
    if (el) {
        const height = el.scrollHeight + 200;
        console.log("Scrolling history pane to bottom, height:", height);
        el.scrollTop = height;
    }
};


const formatAutobotMessage = (text: string): Message => {
    const botMsg: Message = { text: "", type: "bot"};
    if (text.toLowerCase().includes('image')) {
        //emit("showImage", "/img/auen_ref.jpg","Fantasy");
        botMsg.text += "Here is an image of Auenländ.";
        botMsg.src = "/img/auen_ref.jpg";
    }
    if (text.toLowerCase().includes('wiki')) {
        //emit("showImage", "https:\/\/upload.wikimedia.org\/wikipedia\/commons\/thumb\/c\/c6\/Abeille_charpentiere_1024.jpg\/330px-Abeille_charpentiere_1024.jpg","Wiki Bee");
        botMsg.text = "Wiki Bee.";
        botMsg.src = "https:\/\/upload.wikimedia.org\/wikipedia\/commons\/thumb\/c\/c6\/Abeille_charpentiere_1024.jpg\/330px-Abeille_charpentiere_1024.jpg";
    }
    if (text.toLowerCase().includes('audio')) {
        // emit("playAudio", "https:\/\/www.deutsche-digitale-bibliothek.de\/item\/4S5THRPVERDH2DCDJR3WKXJBAPW4EXEP?isThumbnailFiltered=true&query=Tonaufnahme+Eisvogel&rows=20&offset=0&viewType=list&hitNumber=2");
        //emit("playAudio", "https://api.deutsche-digitale-bibliothek.de/binary/aaedf5bc-6ac4-4112-aa42-f4556c5f8ce2.mpeg","Eisvogel Tonaufnahme");
        botMsg.text += "Eisvogel Tonaufnahme";
        botMsg.audioSrc = "https://api.deutsche-digitale-bibliothek.de/binary/aaedf5bc-6ac4-4112-aa42-f4556c5f8ce2.mpeg";
    }
    if (text.toLowerCase().includes('frame')) {
        emit("showFrame", 'https://www.youtube.com/embed/QGbPBJxLg6I', "Rheinauen mit Hund");
    }
    if (text.toLowerCase().includes('link')) {
        botMsg.text += "Nazka Anreise"
        botMsg.link = "https://nazka.de/anreise";
        //chatMessages.value.push(botMsg);
        //autoBot = false;
    }
    if (botMsg.text === "") {
        botMsg.text = "Autobot response to: " + text;
    }
    if (text && text.toLowerCase().startsWith("options")) {
        const items = text.split(" ");
        const options = items.slice(1).map(item => ({title: item.trim(), text: item.trim()}));
        console.log("Parsed options:", options);
        botMsg.text = "Please choose an option:";
        botMsg.options = options;
    }

    return botMsg;
};

const formatBotMessage =  (message: any): Message => {
    const botMsg: Message = {} as Message;
    if (!message.context) {
        console.log("No context in bot message, not appending.");
        loading.value = false;
        return botMsg;
    }
    if (!message.message) {
        console.log("No message in bot message, not appending.");
        loading.value = false;
        return botMsg;
    }
    // message.message field might be array, due to some bug in backend? Handle that: use first element only
    if (Array.isArray(message.message.text)) message.message.text = message.message.text[0];
    if (Array.isArray(message.message.link)) message.message.link = message.message.link[0];
    if (Array.isArray(message.message.audio)) message.message.audio = message.message.audio[0];

    if (message.message.text) 
        botMsg.text = message.message.text || ""
    if (message.message.image) {
        botMsg.src = message.message.image
    }
    if (message.message.audio) {
        botMsg.audioSrc = message.message.audio
    }
    if (message.message.link) {
        botMsg.link = message.message.link.url
        //botMsg.src = message.message.link.url
    }
    if (message.context.options) {
        console.log("Bot message has options:", message.context.options);
        botMsg.options = message.context.options
    }
    if (message.context.options && Array.isArray(message.context.options)) {
        console.log("Bot message has options:", message.context.options);
        botMsg.options = message.context.options;
    }

    botMsg.type = "bot";
    return botMsg

};


const appendChatMessage = async (message: { text: string; type: string }) => {
    if (!message.text) {
        console.log("Empty message, not appending.");
        emit("clear")
        //chatMessages.value = [];
        return;
    }
    loading.value = true;
    console.log("Appending chat message:", message);
    chatMessages.value.push(message);

    scrollHistoryToBottom();

    if (autoBot) {
        const botMsg: Message = formatAutobotMessage(message.text);
        setTimeout(async () => {
            console.log("Appending autobot message:", botMsg);
            chatMessages.value.push(botMsg);
            await scrollHistoryToBottom();
            loading.value = false;
        }, 1000);
    } else {
        console.log("Autobot processing disabled.");
        let postMsg: any
        // find last user input
        let lastUserInput = ""
        const userInputs = chatMessages.value.filter(msg => msg.type === "user");
        if (userInputs.length > 1) {
            const last = userInputs[userInputs.length - 2];
            if (last && typeof last.text === 'string') {
                lastUserInput = last.text;
            }
        }
        console.log("Found previous user inputs:", lastUserInput);
        // need to copy backendData from previous bot message if exists
        const botResponses = chatMessages.value.filter(msg => msg.type === "bot" && msg.backendData);
        console.log("Found previous bot responses with backend data:", botResponses.length, botResponses);
        if (botResponses.length > 0) {
            const lastMsg = botResponses[botResponses.length - 1];
            const lastIntent = lastMsg?.backendData?.context.intent || "";
            postMsg = { ...lastMsg?.backendData}
            postMsg.message = {"text": message.text}
            postMsg.context.last_intent = lastIntent
            postMsg.context.last_input = lastUserInput;
            postMsg.lang = locale.value;
            postMsg.sequence += 1;
            // some advanced context handling could go here
            if (postMsg.context.intent && (!postMsg.context.options || postMsg.context.options.length == 0)) {
                delete postMsg.context.intent;
            }

        } else {
            postMsg = { message:{"text": message.text}, session: "", sequence:1, lang: locale.value, context: {} };
        }

        let backendPostCheck: AxiosResponse<any>;
        const backendPost = await postToBackend(postMsg)
        backendPostCheck = handleBackendResponse(backendPost)
        console.log("APP: Backend post response:", backendPostCheck)
        if (backendPostCheck.status == 200) {
            console.log(`APP: Backend API post completed`);
        } else {
            console.log(`APP: Backend API post error status: ${backendPostCheck.status}`);
        }

        console.log("Recevied:", backendPostCheck.data);
        const botMsg: Message = formatBotMessage(backendPostCheck.data);
        botMsg.backendData = backendPostCheck.data;
        console.log("Appending bot message from backend:", botMsg);
        chatMessages.value.push(botMsg);
        await scrollHistoryToBottom();
        loading.value = false;

    }

    emit('message', message);
};

/*
watch(chatInput, (newInput) => {
    console.log("Chat input changed to:", newInput);
});
*/

const botOption = (opt: string) => {
    console.log("Bot option selected:", opt);
    appendChatMessage({ text: opt, type: 'user' });
}

onMounted(() => {
    console.log("ChatPane mounted");
    // includes stuff for autobot processing
    autoBot = true;
    try {
        const ready = localStorage.getItem('backendReady');
        if (ready === 'true') {
            autoBot = false;
            console.log('Autobot disabled because localStorage.backendReady is true');
        }
    } catch (e) {
        console.warn('Unable to read localStorage.backendReady', e);
    }
});

</script>

<template>
    <div class="chat-pane">
        <div class="history-pane" ref="historyPane">
            <div v-for="(msg, idx) in chatMessages" class="history" :key="idx">
                <VaInput v-if="msg.type == 'user'" :disabled="true" :stateful="true" :placeholder="msg.text"
                    :class="msg.type" />
                <BotResponse v-else :text="msg.text" :src="msg.src" :audioSrc="msg.audioSrc" :link="msg.link"
                    :options="msg.options" @optionSelected="(option: string) => botOption(option)" :idx="idx"
                    :last="idx === chatMessages.length - 1" />
            </div>
        </div>

        <VaInput v-model="chatInput" class="mb-6 input" :placeholder="t('input')" :autofocus="true" :disabled="loading"
            @keyup.enter="appendChatMessage({ text: chatInput, type: 'user' }); chatInput = ''">
            <template #append>
                <VaIcon v-if="loading" name="refresh" spin class="mr-4 ml-4" color="secondary" />
                <VaIcon v-else name="send" class="mr-4 ml-4" color="secondary"
                    @click="appendChatMessage({ text: chatInput, type: 'user' }); chatInput = ''" />
            </template>
        </VaInput>
    </div>

</template>

<style scoped>
.chat-pane {
    padding: 16px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: unset;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
    position: relative;
}

.history-pane {
    /*
    height: calc(100% - 5rem);
    */
    max-height: calc(100% - 6rem);
    width: 100%;
    box-sizing: border-box;
    position: relative;
    overflow-y: scroll;
    position: absolute;
    bottom: 5rem;
}

.input {
    width: 100%;
    color: var(--va-on-background-primary, #000);
    background-color: var(--va-background-primary, #fff);
    border-radius: 8px;
    position: absolute;
    bottom: 1rem;
    left: 0;
    opacity: 1.0;
}

.history {
    width: 90%;
    margin-bottom: 8px;
    border-radius: 8px;
    box-sizing: border-box;
}

.user {
    color: var(--va-primary);
    background-color: var(--va-background-primary);
    margin-left: 1rem;
    width: 90%;
    margin-bottom: 8px;
    border-radius: 8px;
    box-sizing: border-box;
    padding: 4px;
}

.bot {
    margin-right: 1rem;
    width: 90%;
    box-sizing: border-box;
}

.va-input-wrapper--disabled {
    opacity: 1.0;
}
</style>