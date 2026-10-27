<template>
  <main class="min-h-screen grid grid-cols-1 lg:grid-cols-12 bg-[#fffdf9] text-[#1d211e]">
    <!-- Left Visual Panel (Desktop 1024px+) -->
    <section class="hidden lg:flex lg:col-span-5 relative flex-col justify-between p-10 xl:p-14 text-white overflow-hidden bg-[#181c19]">
      <!-- Background Image with Ambient Gradient Overlay -->
      <div
        class="absolute inset-0 bg-cover bg-center transition-transform duration-1000 scale-105"
        style="background-image: url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1400&q=85');"
      ></div>
      <div class="absolute inset-0 bg-linear-to-b from-[#181c19]/70 via-[#181c19]/80 to-[#181c19]/95 backdrop-blur-[2px]"></div>

      <!-- Top Section -->
      <div class="relative z-10">
        <RouterLink
          to="/"
          class="inline-flex items-center gap-2 text-xs font-bold text-white/90 hover:text-[#f47b20] transition bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/15 shadow-sm"
        >
          <ArrowLeft :size="14" />
          <span>Back to Live Web</span>
        </RouterLink>

        <div class="flex items-center gap-2.5 mt-8">
          <div class="w-9 h-9 rounded-xl bg-[#f47b20] flex items-center justify-center text-white font-bold text-base shadow-md">
            🍽️
          </div>
          <div>
            <div class="font-heading font-extrabold text-sm tracking-wider uppercase text-white">
              SHP <span class="text-[#f47b20]">RESTRO OS</span>
            </div>
            <div class="text-[10px] text-gray-400 font-medium uppercase tracking-widest -mt-0.5">
              Next-Gen Management Suite
            </div>
          </div>
        </div>
      </div>

      <!-- Mid Content / Punchy Brand Statement -->
      <div class="relative z-10 space-y-4 my-auto py-8">
        <h1 class="font-heading text-4xl xl:text-5xl font-extrabold tracking-tight leading-tight">
          Good food.<br />
          <span class="text-[#f47b20]">Great moments.</span>
        </h1>
        <p class="text-gray-300 text-sm xl:text-base leading-relaxed max-w-sm">
          {{ description }}
        </p>

        <!-- Feature Badges -->
        <div class="pt-4 space-y-2.5">
          <div class="flex items-center gap-2.5 text-xs text-gray-200">
            <span class="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">✓</span>
            <span>Real-time Table Orders & POS Billing</span>
          </div>
          <div class="flex items-center gap-2.5 text-xs text-gray-200">
            <span class="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">✓</span>
            <span>Live Kitchen Display System (KDS) Tickets</span>
          </div>
          <div class="flex items-center gap-2.5 text-xs text-gray-200">
            <span class="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">✓</span>
            <span>Automated Delivery Dispatch & Analytics</span>
          </div>
        </div>
      </div>

      <!-- Bottom Caption -->
      <div class="relative z-10 pt-4 border-t border-white/10 flex items-center justify-between text-[11px] text-gray-400">
        <span>SHP Restaurant OS v2.0</span>
        <span class="flex items-center gap-1.5 text-emerald-400 font-semibold">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          System Online
        </span>
      </div>
    </section>

    <!-- Right Form Panel (Mobile, Tablet, Desktop) -->
    <section class="lg:col-span-7 flex flex-col justify-between p-4 sm:p-8 lg:p-12 xl:p-16 relative">
      <!-- Mobile Top Navigation Header -->
      <div class="flex items-center justify-between lg:hidden mb-6">
        <RouterLink
          to="/"
          class="inline-flex items-center gap-1.5 text-xs font-bold text-gray-700 hover:text-[#f47b20] bg-gray-100 px-3.5 py-2 rounded-xl transition"
        >
          <ArrowLeft :size="14" />
          <span>Back to Web</span>
        </RouterLink>

        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-lg bg-[#f47b20] flex items-center justify-center text-white text-xs font-bold">
            🍽️
          </div>
          <span class="font-heading font-extrabold text-sm text-gray-900">SHP RESTRO</span>
        </div>
      </div>

      <!-- Centered Form Container -->
      <div class="max-w-md w-full mx-auto my-auto py-4">
        <!-- Eyebrow & Title -->
        <div class="mb-6 sm:mb-8 text-left">
          <span class="inline-block text-[11px] font-bold text-[#f47b20] uppercase tracking-widest bg-orange-50 px-2.5 py-1 rounded-md border border-orange-100">
            {{ eyebrow }}
          </span>
          <h2 class="font-heading text-2xl sm:text-3xl font-extrabold text-gray-900 mt-2 tracking-tight">
            {{ title }}
          </h2>
          <p class="text-xs sm:text-sm text-gray-500 mt-1.5 leading-relaxed">
            {{ description }}
          </p>
        </div>

        <!-- Form Slot Container -->
        <div class="bg-white rounded-2xl sm:rounded-3xl border border-gray-200/80 p-5 sm:p-8 shadow-xs">
          <slot />
        </div>
      </div>

      <!-- Footer Help Info -->
      <div class="text-center text-xs text-gray-400 pt-6">
        Need assistance? Contact support at <a href="mailto:support@shprestaurant.com" class="text-[#f47b20] hover:underline">support@shprestaurant.com</a>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'

defineProps<{
  eyebrow: string
  title: string
  description: string
}>()
</script>
