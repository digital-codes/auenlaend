<script setup lang="ts">
import type { Ref } from 'vue'
import { ref, watch, onMounted, computed } from 'vue';

import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales } = useI18n();

import { useBreakpoint } from 'vuestic-ui';

/* theme switch: https://ui.vuestic.dev/styles/colors */
import { useColors } from "vuestic-ui";
const breakpoints = useBreakpoint()

const showSidebar = ref(false)
const page = ref(1)

import ChatBot from './components/ChatBot.vue'
import IntroPage from './components/IntroPage.vue'

import { postToBackend, getFromBackend, handleBackendResponse } from './services/backendComms'

// ----------------------------
// load sidebar icons
import icon1_l from "@/assets/icons/weather.svg?url"
import icon2_l from "@/assets/icons/house.svg?url"
import icon1_d from "@/assets/icons/weather_d.svg?url"
import icon2_d from "@/assets/icons/house_d.svg?url"
const icons = ref({
  "icon1": icon1_l,
  "icon2": icon2_l
})

import logo from '@/assets/img/auenlaend_square.png'

const langSel = ref("")
//locale.value = langSel
console.log(availableLocales)
const languages = availableLocales

// initialize from localStorage (language + theme) and apply sensible fallbacks
const safeGet = (key: string) => {
  try { return localStorage.getItem(key) } catch { return null }
}


// mode switch 
const { applyPreset, currentPresetName } = useColors();


const modeSwitch = computed({
  get() {
    return currentPresetName.value
  },
  set(value) {
    applyPreset(value)
    // set color-scheme for non-vuestic components
    if (value === "dark") {
      document.body.style.setProperty('color-scheme', 'dark')
      icons.value = {
        "icon1": icon1_d,
        "icon2": icon2_d,
      }
    } else {
      document.body.style.setProperty('color-scheme', 'light')
      icons.value = {
        "icon1": icon1_l,
        "icon2": icon2_l,
      }
    }
    localStorage.setItem('theme', value);
  }
})

watch(langSel, (newLang) => {
  locale.value = newLang
  localStorage.setItem('language', newLang);
  langSel.value = newLang
})

const goto = (p: number) => {
  page.value = p
  showSidebar.value = false
}

onMounted(async () => {
  // language
  const savedLang = safeGet('language')
  const browserLang = navigator?.language?.split('-')?.[0]
  const pickLang = (l?: string | null) => (l && availableLocales.includes(l) ? l : undefined)

  const initialLang = pickLang(savedLang) ?? pickLang(browserLang) ?? availableLocales[0]
  if (initialLang) {
    locale.value = initialLang
    // langSel is declared later in the setup; it's safe to set here inside onMounted
    try { (langSel as Ref<string>).value = initialLang } catch { }
  }

  // theme/preset
  const savedTheme = safeGet('theme')
  if (savedTheme) {
    try {
      // applyPreset is created later in the setup; calling it onMounted is safe
      if (typeof applyPreset === 'function') applyPreset(savedTheme)
      document.body.style.setProperty('color-scheme', savedTheme === 'dark' ? 'dark' : 'light')
    } catch (e) {
      // ignore if applyPreset isn't available yet or fails
    }
  }


  // make a check if backend is running at /api/ with a get request. should return 200 and {status: "ok"}
  /*
  fetch('/api').then(response => {
    if (!response.ok) {
      console.error("APP: Backend API is not reachable:", response.statusText);
    } else {
      console.log("APP: Backend API is reachable.");
      response.json().then(data => {
        if (data.status === "ok") {
          console.log("APP: Backend API status:", data.status);
        } else {
          console.error("APP: Backend API returned unexpected status:", data);
        }
      }).catch(error => {
        console.error("APP: Error parsing Backend API response:", error);
      });
    }
  }).catch(error => {
    console.error("APP: Error while trying to reach Backend API:", error);
  });
  */

  const backendComms = await getFromBackend()
  if (!backendComms || !backendComms.data) {
    console.error("APP: No response from Backend API");
    try {
      localStorage.setItem('backendReady', 'false')
      console.log('APP: localStorage backendReady set to false')
    } catch (e) {
      console.error('APP: Failed to set localStorage backendReady', e)
    }
    return
  } else {
    console.log("APP: Received response from Backend API:", backendComms)
    const backendCheck = handleBackendResponse(backendComms)
    console.log("APP: Backend check response:", backendCheck)
    if (backendCheck.data.status === "ok") {
      console.log("APP: Backend API status:", backendCheck.data.status);
      try {
        localStorage.setItem('backendReady', 'true')
        console.log('APP: localStorage backendReady set to true')
      } catch (e) {
        console.error('APP: Failed to set localStorage backendReady', e)
      }
      // try a dummy post
      const dummyPost = { input: "wie macht man co2 messung", session: "", repeat: true, context: { "lang": "de", "type": "123", "history": "bla bla" } }
      for (const repeat of [false, true]) {
        dummyPost.repeat = repeat
        console.log(`APP: Sending dummy post to backend with repeat=${repeat}:`, dummyPost)
        const backendPost = await postToBackend(dummyPost, repeat)
        const backendPostCheck = handleBackendResponse(backendPost)
        console.log("APP: Backend dummy post response:", backendPostCheck)
        if (backendPostCheck.data.status) {
          console.log(`APP: Backend API dummy post completed with repeat=${repeat}`);
        } else {
          console.log(`APP: Backend API dummy post delayed with repeat=${repeat}`);
        }
      }
    } else {
      console.error("APP: Backend API returned unexpected status:", backendCheck.data.status);
      try {
        localStorage.setItem('backendReady', 'false')
        console.log('APP: localStorage backendReady set to false')
      } catch (e) {
        console.error('APP: Failed to set localStorage backendReady', e)
      }
    }
  }
})


// ----------------------------
type MsgType = { text: string; type: string };

const msg = (message: MsgType) => {
  console.log("APP: Received message from ChatBot:", message);
};


</script>

<template>
  <VaLayout style="height: 100%">
    <template #top>
      <VaNavbar color="primary" class="py-2">
        <template #left>
          <VaButton :icon="showSidebar ? 'menu_open' : 'menu'" @click="showSidebar = !showSidebar" size="large"
            :title="t('menu')" role="switch" :aria-checked="showSidebar ? 'true' : 'false'" />
        </template>

        <template #center>
          <VaNavbarItem><span class="headline left">{{ $t("rheinauen") }}</span></VaNavbarItem>
          <VaNavbarItem role="link" aria-label="Click for Home">
            <VaImage :src="logo" :title='t("logo")' fit="cover" class="logoimg" @click="page = 1"
              style="cursor: pointer">
            </VaImage>
          </VaNavbarItem>
          <VaNavbarItem v-if="breakpoints.smUp"><span class="headline right">{{ $t("chatbot") }}</span></VaNavbarItem>
        </template>
        <template #right>
          <div class="langselect">
            <VaSelect contentClass="selection" v-model="langSel" :options="languages" :placeholder="langSel">
              <template #prepend>
                <VaIcon name="translate" class="xlate" />
              </template>
            </VaSelect>
          </div>
          <VaButton round :icon="modeSwitch == 'dark' ? 'dark_mode' : 'light_mode'"
            @click="modeSwitch = modeSwitch == 'dark' ? 'light' : 'dark'" :title='t("mode")' role="switch"
            :aria-checked="modeSwitch == 'dark' ? 'true' : 'false'" />
        </template>

      </VaNavbar>
    </template>

    <template #left>
      <VaSidebar v-model="showSidebar" class="py-4">
        <VaSidebarItem :active="page === 1" @click="goto(1)">
          <VaSidebarItemContent>
            <VaIcon name="info" />
            <VaSidebarItemTitle>
              {{ $t("info") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem :active="page === 2" @click="goto(2)">
          <VaSidebarItemContent>
            <VaIcon name="explore" />
            <VaSidebarItemTitle>
              {{ $t("chatbot") }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
      </VaSidebar>
    </template>

    <template #content>
      <main v-if="page === 1" class="p-4 main-info">
        <IntroPage @start="page = 2" />
      </main>
      <main v-else-if="page === 2" class="p-4 main-chat">
        <ChatBot @message="msg" />
      </main>
    </template>
  </VaLayout>

</template>

<style scoped>
.va-navbar {
  height: 4rem;
}

.va-sidebar {
  top: 4rem;
}

.logoimg {
  height: 3rem;
  width: 3rem;
  border-width: 4px;
  border-style: solid;
  border-radius: 1rem;
  margin-left: .5rem;
  margin-right: .5rem;
}

main {
  height: 100%;
  overflow: auto;
}

.main-info {
  /* styles for info page */
  overflow-y: scroll;
}

.main-chat {
  /* styles for chat page */
}

.langselect {
  max-width: 6rem;
  margin-right: 8px;
}
</style>