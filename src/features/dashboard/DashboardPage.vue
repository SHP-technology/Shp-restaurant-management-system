<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import {
  LayoutDashboard,
  ShoppingBag,
  Grid,
  Calendar,
  Truck,
  PartyPopper,
  UtensilsCrossed,
  Users,
  BarChart2,
  Settings as SettingsIcon,
  LogOut,
  ChevronDown,
  TrendingUp,
  Download,
  Edit2,
  Trash2,
  Search,
  CheckCircle,
  Menu as MenuIcon,
  X,
  Phone,
  RefreshCw,
  Plus,
} from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import {
  restroHandler,
  type TableData,
  type OrderData,
  type ReservationData,
  type PartyBookingData,
  type MenuItemData,
  type CustomerData,
} from '../../services/api'
import { getApiErrorMessage } from '../../services/api/client'

const authStore = useAuthStore()
const router = useRouter()

const activeTab = ref('Dashboard')
const orderFilter = ref('All')
const searchQuery = ref('')
const mobileMenuOpen = ref(false)

async function handleLogout() {
  await restroHandler.auth.logout()
  authStore.clearSession()
  router.push('/')
}

const sidebarItems = [
  { name: 'Dashboard', icon: LayoutDashboard, badge: null },
  { name: 'Orders', icon: ShoppingBag, badge: '6' },
  { name: 'Table Management', icon: Grid, badge: null },
  { name: 'Reservations', icon: Calendar, badge: null },
  { name: 'Delivery Orders', icon: Truck, badge: null },
  { name: 'Party Bookings', icon: PartyPopper, badge: null },
  { name: 'Menu Management', icon: UtensilsCrossed, badge: null },
  { name: 'Customers', icon: Users, badge: null },
  { name: 'Reports', icon: BarChart2, badge: null },
  { name: 'Settings', icon: SettingsIcon, badge: null },
]

type StatCard = {
  label: string
  value: string
  sub1: string
  sub2: string
  icon: typeof ShoppingBag
  color: string
}

type ReportsData = {
  monthlyRevenue: string
  monthlyGrowth: string
  averageOrderValue: string
  aovGrowth: string
  topCategory: string
  topCategoryShare: string
  todayRevenue?: string
  revenueGrowth?: string
}

// Dashboard Stats (populated only from the API)
const stats = ref<StatCard[]>([])

// Live Orders (populated only from the API)
const liveOrders = ref<OrderData[]>([])

// Table Management State (populated only from the API)
const tableList = ref<TableData[]>([])

// Reservations State (populated only from the API)
const reservations = ref<ReservationData[]>([])

// Delivery Orders State (populated only from the API)
const deliveryList = ref<OrderData[]>([])

// Party Bookings State (populated only from the API)
const parties = ref<PartyBookingData[]>([])

// Menu Management State (populated only from the API)
const menuItemsList = ref<MenuItemData[]>([])

// Customers State (populated only from the API)
const customers = ref<CustomerData[]>([])

// Settings State
const restaurantId = ref<string | null>(null)
const outletName = ref('')
const gstRate = ref('')
const autoAccept = ref(true)
const settingsSaved = ref(false)
const settingsError = ref('')

// Reports State (populated only from the API)
const reportsData = ref<ReportsData | null>(null)

// Global load / error state
const isLoading = ref(true)
const error = ref('')

// Table legend counts derived from real table data
const tableCounts = computed(() => ({
  available: tableList.value.filter((t) => t.status === 'Available').length,
  booked: tableList.value.filter((t) => t.status === 'Booked').length,
  occupied: tableList.value.filter((t) => t.status === 'Occupied').length,
}))

// Filtered Live Orders
const filteredOrders = computed(() => {
  return liveOrders.value.filter((o) => {
    const matchesFilter = orderFilter.value === 'All' || o.type === orderFilter.value
    const matchesSearch =
      !searchQuery.value ||
      o.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (o.customer && o.customer.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (o.items && o.items.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchesFilter && matchesSearch
  })
})

function getStatusColor(status: string) {
  if (status === 'Ready') return 'bg-emerald-100 text-emerald-700'
  if (status === 'Preparing') return 'bg-[#f47b20]/20 text-[#f47b20]'
  if (status === 'Completed' || status === 'Delivered') return 'bg-gray-100 text-gray-700'
  if (status === 'Out for Delivery') return 'bg-indigo-100 text-indigo-700'
  return 'bg-blue-100 text-blue-700'
}

async function handleSaveSettings() {
  settingsError.value = ''
  if (!restaurantId.value) {
    settingsError.value = 'No restaurant is loaded yet. Please wait for data to load and try again.'
    return
  }
  try {
    await restroHandler.restaurants.update(restaurantId.value, {
      outlet_name: outletName.value,
      gst_rate: gstRate.value,
      auto_accept: autoAccept.value,
    })
    settingsSaved.value = true
    setTimeout(() => {
      settingsSaved.value = false
    }, 2500)
  } catch (err) {
    settingsError.value = getApiErrorMessage(err)
  }
}

async function handleToggleStock(itemId: number) {
  // Reflect the server response only after it succeeds — never fake it.
  try {
    await restroHandler.menu.toggleStock(itemId)
    menuItemsList.value = menuItemsList.value.map((item) => {
      if (item.id === itemId) {
        const nextStatus = item.status === 'In Stock' ? 'Out of Stock' : 'In Stock'
        return { ...item, status: nextStatus }
      }
      return item
    })
  } catch (err) {
    error.value = getApiErrorMessage(err)
  }
}

async function loadDashboard() {
  isLoading.value = true
  error.value = ''

  const results = await Promise.allSettled([
    // 1. Stats & Reports
    restroHandler.analytics.getDashboardStats().then((data) => {
      if (data?.stats) {
        stats.value = data.stats.map((s, idx) => ({
          ...s,
          icon: sidebarItems[idx]?.icon || ShoppingBag,
          color: idx === 0 ? 'text-blue-600 bg-blue-50' : idx === 1 ? 'text-[#f47b20] bg-orange-50' : idx === 2 ? 'text-emerald-600 bg-emerald-50' : 'text-purple-600 bg-purple-50'
        }))
      }
      if (data?.reports) reportsData.value = data.reports
    }),

    // 2. Restaurant & Settings
    restroHandler.restaurants.getCurrent().then((rest) => {
      if (rest) {
        if (rest.id) restaurantId.value = rest.id
        if (rest.outlet_name) outletName.value = rest.outlet_name
        if (rest.gst_rate) gstRate.value = rest.gst_rate
        if (rest.auto_accept !== undefined) autoAccept.value = rest.auto_accept
      }
    }),

    // 3. Orders
    restroHandler.orders.list().then((data) => {
      if (Array.isArray(data)) {
        const formatted = data.map((o) => ({
          ...o,
          statusColor: getStatusColor(o.status),
        }))
        liveOrders.value = formatted
        deliveryList.value = formatted.filter((o) => o.type === 'Delivery' || o.order_type === 'Delivery')
      }
    }),

    // 4. Tables
    restroHandler.tables.list().then((data) => {
      if (Array.isArray(data)) {
        tableList.value = data.map((t) => ({
          id: t.id,
          num: t.num,
          status: t.status,
          seats: t.seats || 4,
        }))
      }
    }),

    // 5. Reservations
    restroHandler.reservations.listTableReservations().then((data) => {
      if (Array.isArray(data)) reservations.value = data
    }),

    // 6. Party Bookings
    restroHandler.reservations.listPartyBookings().then((data) => {
      if (Array.isArray(data)) parties.value = data
    }),

    // 7. Menu items
    restroHandler.menu.list().then((data) => {
      if (Array.isArray(data)) menuItemsList.value = data
    }),

    // 8. Customers
    restroHandler.customers.list().then((data) => {
      if (Array.isArray(data)) customers.value = data
    }),
  ])

  const firstError = results.find((r): r is PromiseRejectedResult => r.status === 'rejected')
  if (firstError) {
    error.value = getApiErrorMessage(firstError.reason)
  }

  isLoading.value = false
}

onMounted(async () => {
  await loadDashboard()

  // WebSocket real-time updates
  try {
    restroHandler.realtime.connect('default')
    restroHandler.realtime.on('order.created', () => {
      restroHandler.orders.list().then((d) => {
        if (d && Array.isArray(d)) {
          liveOrders.value = d.map((o) => ({ ...o, statusColor: getStatusColor(o.status) }))
        }
      })
    })
    restroHandler.realtime.on('table.status_updated', () => {
      restroHandler.tables.list().then((d) => {
        if (d && Array.isArray(d)) tableList.value = d
      })
    })
  } catch {}
})

onUnmounted(() => {
  restroHandler.realtime.disconnect()
})

function toggleTableStatus(num: number) {
  const target = tableList.value.find((t) => t.num === num)
  if (!target) return
  const previousStatus = target.status
  const nextStatus: TableData['status'] =
    previousStatus === 'Available' ? 'Booked' : previousStatus === 'Booked' ? 'Occupied' : 'Available'

  // Optimistic update, reverted if the server rejects it.
  tableList.value = tableList.value.map((t) =>
    t.num === num ? { ...t, status: nextStatus } : t
  )

  restroHandler.tables.update(target.id || num, { status: nextStatus }).catch((err) => {
    error.value = getApiErrorMessage(err)
    tableList.value = tableList.value.map((t) =>
      t.num === num ? { ...t, status: previousStatus } : t
    )
  })
}

function handleUpdateOrderStatus(orderId: string, currentStatus: string) {
  const nextStatus =
    currentStatus === 'New'
      ? 'Preparing'
      : currentStatus === 'Preparing'
      ? 'Ready'
      : currentStatus === 'Ready'
      ? 'Completed'
      : 'New'

  // Only reflect the new status after the server confirms it.
  restroHandler.orders
    .updateStatus(orderId, nextStatus)
    .then(() => {
      liveOrders.value = liveOrders.value.map((o) =>
        o.id === orderId ? { ...o, status: nextStatus, statusColor: getStatusColor(nextStatus) } : o
      )
    })
    .catch((err) => {
      error.value = getApiErrorMessage(err)
    })
}
</script>

<template>
  <div class="min-h-screen bg-slate-100/70 text-slate-900 flex flex-col md:flex-row font-sans selection:bg-orange-500 selection:text-white">
    <!-- Mobile Header Bar for small screens -->
    <div class="md:hidden bg-white text-slate-900 p-4 flex items-center justify-between sticky top-0 z-40 border-b border-slate-200 shadow-2xs">
      <RouterLink to="/" class="flex items-center gap-2">
        <span class="font-heading text-lg font-black tracking-tight text-slate-900">
          SHP <span class="text-orange-600">POS</span>
        </span>
      </RouterLink>

      <div class="flex items-center gap-3">
        <span class="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold">
          ● Live
        </span>
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="p-1.5 rounded-lg bg-slate-100 text-slate-700 hover:text-slate-900 border border-slate-200"
        >
          <X v-if="mobileMenuOpen" :size="20" />
          <MenuIcon v-else :size="20" />
        </button>
      </div>
    </div>

    <!-- Mobile Drawer Navigation -->
    <div
      v-if="mobileMenuOpen"
      class="md:hidden fixed inset-0 z-30 bg-slate-900/40 backdrop-blur-xs flex flex-col"
      @click.self="mobileMenuOpen = false"
    >
      <div class="w-4/5 max-w-xs bg-white text-slate-800 h-full p-5 space-y-4 flex flex-col justify-between overflow-y-auto border-r border-slate-200 shadow-2xl">
        <div>
          <p class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">POS Navigation</p>
          <nav class="space-y-1">
            <button
              v-for="item in sidebarItems"
              :key="item.name"
              @click="activeTab = item.name; mobileMenuOpen = false"
              :class="[
                'w-full flex items-center justify-between px-3.5 py-3 rounded-xl transition text-xs font-semibold cursor-pointer',
                activeTab === item.name
                  ? 'bg-orange-600 text-white font-bold shadow-sm'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              ]"
            >
              <div class="flex items-center gap-3">
                <component :is="item.icon" :size="16" />
                <span>{{ item.name }}</span>
              </div>
              <span v-if="item.badge" class="rounded-full bg-rose-500 px-1.5 py-0.5 text-[9px] font-bold text-white">
                {{ item.badge }}
              </span>
            </button>
          </nav>
        </div>

        <div class="pt-4 border-t border-slate-200 space-y-2">
          <RouterLink to="/" class="block text-xs text-slate-500 hover:text-slate-900 underline">
            Back to Public Website
          </RouterLink>
          <button
            @click="handleLogout"
            class="w-full flex items-center gap-2 py-2 text-xs font-bold text-rose-600 hover:text-rose-700"
          >
            <LogOut :size="15" />
            <span>Logout Staff Session</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Desktop Sidebar -->
    <aside class="hidden md:flex w-64 bg-white text-slate-800 border-r border-slate-200 flex-col justify-between p-4 shrink-0 shadow-xs sticky top-0 h-screen">
      <div>
        <!-- Logo Brand -->
        <div class="flex items-center justify-between pb-5 border-b border-slate-200">
          <RouterLink to="/" class="flex items-center gap-2.5">
            <span class="font-heading text-xl font-black tracking-tight text-slate-900">
              SHP <span class="text-orange-600">POS</span>
            </span>
          </RouterLink>
          <RouterLink to="/" class="text-[10px] text-slate-500 hover:text-slate-900 underline">
            Website →
          </RouterLink>
        </div>

        <!-- Navigation items list -->
        <nav class="mt-4 space-y-1 text-xs">
          <button
            v-for="item in sidebarItems"
            :key="item.name"
            @click="activeTab = item.name"
            :class="[
              'w-full flex items-center justify-between px-3 py-2.5 rounded-xl transition font-medium cursor-pointer',
              activeTab === item.name
                ? 'bg-orange-600 text-white font-bold shadow-sm'
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
            ]"
          >
            <div class="flex items-center gap-2.5">
              <component :is="item.icon" :size="16" />
              <span>{{ item.name }}</span>
            </div>
            <span v-if="item.badge" class="rounded-full bg-rose-500 px-1.5 py-0.5 text-[9px] font-bold text-white">
              {{ item.badge }}
            </span>
          </button>
        </nav>
      </div>

      <!-- Logout & Staff Info -->
      <div class="pt-4 border-t border-slate-200">
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold text-slate-600 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition cursor-pointer"
        >
          <LogOut :size="16" />
          <span>Logout Staff</span>
        </button>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 p-3.5 sm:p-6 lg:p-8 space-y-6 overflow-x-hidden min-w-0">
      <!-- Header Bar -->
      <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 sm:p-5 rounded-2xl border border-gray-200/90 shadow-xs">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-[10px] font-bold uppercase tracking-wider text-[#f47b20]">Outlet Control Room</span>
            <span class="text-gray-300">•</span>
            <span class="text-xs font-semibold text-gray-600">{{ activeTab }}</span>
          </div>
          <h1 class="font-heading text-xl sm:text-2xl font-black text-gray-900 mt-0.5">{{ activeTab }} Overview</h1>
        </div>

        <div class="flex flex-wrap items-center gap-2.5 sm:gap-3">
          <div class="flex items-center gap-2 bg-gray-50 border border-gray-200 px-3 py-1.5 rounded-xl text-xs font-bold text-gray-700">
            <span>Today, 28 May</span>
            <ChevronDown :size="13" />
          </div>

          <span class="rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1 text-xs font-bold flex items-center gap-1.5 shadow-2xs">
            <span class="h-2 w-2 rounded-full bg-emerald-600 animate-pulse"></span>
            <span>Live POS Sync</span>
          </span>
        </div>
      </header>

      <!-- Global Loading Indicator -->
      <div
        v-if="isLoading"
        class="flex items-center justify-center gap-2.5 bg-white p-4 rounded-2xl border border-gray-200/90 shadow-xs text-xs font-bold text-gray-600"
      >
        <RefreshCw :size="15" class="animate-spin text-[#f47b20]" />
        <span>Loading live outlet data…</span>
      </div>

      <!-- Global Error Banner with Retry -->
      <div
        v-else-if="error"
        class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-rose-50 p-4 rounded-2xl border border-rose-200 text-xs font-bold text-rose-700"
      >
        <span>{{ error }}</span>
        <button
          @click="loadDashboard"
          class="rounded-xl bg-rose-600 px-3.5 py-1.5 text-white hover:bg-rose-700 transition flex items-center gap-1.5 shrink-0 cursor-pointer active:scale-95"
        >
          <RefreshCw :size="13" /> Retry
        </button>
      </div>

      <!-- TAB 1: DASHBOARD -->
      <div v-if="activeTab === 'Dashboard'" class="space-y-6">
        <!-- Top 4 Stat Metric Cards -->
        <p v-if="!isLoading && stats.length === 0" class="text-xs text-gray-500 bg-white p-4 rounded-2xl border border-gray-200/90 shadow-xs">
          No dashboard metrics available yet.
        </p>
        <section v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div
            v-for="stat in stats"
            :key="stat.label"
            class="bg-white p-4 sm:p-5 rounded-2xl border border-gray-200/90 shadow-xs flex flex-col justify-between hover:shadow-md transition-shadow"
          >
            <div class="flex items-center justify-between">
              <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wider">{{ stat.label }}</p>
              <div :class="['w-9 h-9 rounded-xl flex items-center justify-center font-bold', stat.color]">
                <component :is="stat.icon" :size="18" />
              </div>
            </div>
            
            <div class="mt-3">
              <p class="text-2xl sm:text-3xl font-black text-gray-900 font-heading">{{ stat.value }}</p>
              <div class="flex items-center gap-1.5 mt-1 text-[11px] font-bold">
                <span class="text-emerald-600">{{ stat.sub1 }}</span>
                <span class="text-gray-400 font-medium">{{ stat.sub2 }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Live Orders & Table Floor Layout Grid -->
        <section class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <!-- Live Orders Pipeline -->
          <div class="lg:col-span-6 bg-white p-4 sm:p-5 rounded-2xl border border-gray-200/90 shadow-xs space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-100 pb-3">
              <h2 class="font-heading text-base font-black text-gray-900">Live Kitchen Queue</h2>
              <div class="flex items-center gap-1 text-[10px] font-bold text-gray-600 bg-gray-100 p-1 rounded-xl overflow-x-auto max-w-full">
                <button
                  v-for="f in ['All', 'Dine In', 'Delivery', 'Takeaway']"
                  :key="f"
                  @click="orderFilter = f"
                  :class="[
                    'px-2.5 py-1 rounded-lg transition shrink-0 cursor-pointer',
                    orderFilter === f ? 'bg-white text-[#f47b20] shadow-xs font-bold' : 'hover:text-gray-900'
                  ]"
                >
                  {{ f }}
                </button>
              </div>
            </div>

            <div class="space-y-2.5 max-h-[420px] overflow-y-auto pr-1">
              <div
                v-for="order in liveOrders.filter((o) => orderFilter === 'All' || o.type === orderFilter)"
                :key="order.id"
                class="flex items-center justify-between p-3 sm:p-3.5 rounded-xl border border-gray-100 bg-gray-50/70 hover:bg-orange-50/30 transition text-xs"
              >
                <div>
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-gray-900">{{ order.id }}</span>
                    <span class="text-gray-500 font-semibold text-[11px]">({{ order.type }})</span>
                    <span class="font-bold text-[#f47b20]">{{ order.price }}</span>
                  </div>
                  <p class="text-[11px] text-gray-600 mt-0.5 font-medium">{{ order.items }}</p>
                  <p class="text-[10px] text-gray-400 mt-0.5">{{ order.customer }}</p>
                </div>

                <div class="flex items-center gap-2">
                  <span :class="['px-2.5 py-1 rounded-lg text-[10px] font-bold', order.statusColor]">
                    {{ order.status }}
                  </span>
                  <button
                    @click="handleUpdateOrderStatus(order.id, order.status)"
                    class="p-1.5 rounded-lg bg-gray-900 text-white hover:bg-[#f47b20] transition active:scale-95 text-[10px]"
                    title="Advance Status"
                  >
                    <RefreshCw :size="12" />
                  </button>
                </div>
              </div>

              <p
                v-if="!isLoading && liveOrders.filter((o) => orderFilter === 'All' || o.type === orderFilter).length === 0"
                class="text-xs text-gray-400 text-center py-6"
              >
                No orders in the queue right now.
              </p>
            </div>
          </div>

          <!-- Table Floor Status & Revenue Card -->
          <div class="lg:col-span-6 space-y-6">
            <div class="bg-white p-4 sm:p-5 rounded-2xl border border-gray-200/90 shadow-xs space-y-4">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-100 pb-3">
                <h2 class="font-heading text-base font-black text-gray-900">Floor Layout Status</h2>
                <div class="flex items-center gap-2 text-[10px] font-bold flex-wrap">
                  <span class="text-emerald-600">● Available</span>
                  <span class="text-[#f47b20]">● Booked</span>
                  <span class="text-rose-600">● Occupied</span>
                </div>
              </div>

              <!-- Interactive Table Grid -->
              <div v-if="tableList.length" class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button
                  v-for="t in tableList"
                  :key="t.num"
                  @click="toggleTableStatus(t.num)"
                  :class="[
                    'h-13 rounded-xl flex flex-col items-center justify-center font-bold text-xs border transition cursor-pointer active:scale-95',
                    t.status === 'Booked'
                      ? 'bg-orange-500 text-white border-orange-600 shadow-xs'
                      : t.status === 'Occupied'
                      ? 'bg-rose-500 text-white border-rose-600 shadow-xs'
                      : 'bg-white text-gray-700 border-gray-200 hover:border-emerald-500'
                  ]"
                >
                  <span class="text-xs font-black">T{{ t.num }}</span>
                  <span class="text-[9px] opacity-85">{{ t.seats }} Seats</span>
                </button>
              </div>
              <p v-else-if="!isLoading" class="text-xs text-gray-400 text-center py-6">
                No tables configured yet.
              </p>
            </div>

            <!-- Revenue KPI Card -->
            <div v-if="reportsData" class="bg-white p-5 rounded-2xl border border-gray-200/90 shadow-xs flex items-center justify-between">
              <div>
                <p class="text-xs font-bold text-gray-500 uppercase tracking-wider">Today's Total Sales</p>
                <p class="text-2xl sm:text-3xl font-black text-gray-900 mt-1 font-heading">{{ reportsData.todayRevenue || '—' }}</p>
              </div>
              <div v-if="reportsData.revenueGrowth" class="flex items-center gap-1.5 text-emerald-700 bg-emerald-50 px-3.5 py-2 rounded-xl text-xs font-bold border border-emerald-200">
                <TrendingUp :size="16" />
                <span>{{ reportsData.revenueGrowth }}</span>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- TAB 2: ORDERS -->
      <div v-if="activeTab === 'Orders'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-100 pb-4">
          <h2 class="font-heading text-lg font-black text-gray-900">All Kitchen & POS Orders</h2>
          <div class="flex items-center gap-2">
            <div class="relative">
              <Search :size="14" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search ID or Customer..."
                class="rounded-xl border border-gray-200 bg-gray-50 pl-8 pr-3 py-1.5 text-xs focus:border-[#f47b20] focus:bg-white focus:outline-none"
              />
            </div>
            <button class="rounded-xl bg-[#f47b20] px-3.5 py-1.5 text-xs font-bold text-white shadow-xs hover:bg-[#d9630f] transition flex items-center gap-1 shrink-0">
              <Plus :size="13" /> POS Order
            </button>
          </div>
        </div>

        <div class="overflow-x-auto -mx-4 sm:mx-0">
          <table class="w-full text-left text-xs border-collapse min-w-[640px]">
            <thead>
              <tr class="border-b bg-gray-50/80 text-gray-600 uppercase font-bold text-[11px]">
                <th class="p-3.5">Order ID</th>
                <th class="p-3.5">Customer / Table</th>
                <th class="p-3.5">Items</th>
                <th class="p-3.5">Type</th>
                <th class="p-3.5">Total</th>
                <th class="p-3.5">Status</th>
                <th class="p-3.5">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="o in filteredOrders" :key="o.id" class="hover:bg-gray-50/60 transition">
                <td class="p-3.5 font-bold text-gray-900">{{ o.id }}</td>
                <td class="p-3.5 font-semibold text-gray-700">{{ o.customer }}</td>
                <td class="p-3.5 text-gray-600 max-w-xs truncate">{{ o.items }}</td>
                <td class="p-3.5 text-gray-500 font-semibold">{{ o.type }}</td>
                <td class="p-3.5 font-black text-[#f47b20]">{{ o.price }}</td>
                <td class="p-3.5">
                  <span :class="['px-2.5 py-1 rounded-lg text-[10px] font-bold inline-block', o.statusColor]">
                    {{ o.status }}
                  </span>
                </td>
                <td class="p-3.5">
                  <button
                    @click="handleUpdateOrderStatus(o.id, o.status)"
                    class="rounded-lg bg-gray-900 px-2.5 py-1 text-[10px] font-bold text-white hover:bg-[#f47b20] transition active:scale-95 cursor-pointer"
                  >
                    Advance
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-if="!isLoading && filteredOrders.length === 0" class="text-xs text-gray-400 text-center py-8">
            No orders to display.
          </p>
        </div>
      </div>

      <!-- TAB 3: TABLE MANAGEMENT -->
      <div v-if="activeTab === 'Table Management'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-100 pb-4">
          <div>
            <h2 class="font-heading text-lg font-black text-gray-900">Floor Layout & Seating Control</h2>
            <p class="text-xs text-gray-500">Tap table cards to cycle status: Available &rarr; Booked &rarr; Occupied</p>
          </div>

          <div class="flex items-center gap-3 text-xs font-bold flex-wrap">
            <span class="flex items-center gap-1.5 text-emerald-600"><span class="h-3 w-3 rounded-full bg-emerald-500" /> Available ({{ tableCounts.available }})</span>
            <span class="flex items-center gap-1.5 text-[#f47b20]"><span class="h-3 w-3 rounded-full bg-[#f47b20]" /> Booked ({{ tableCounts.booked }})</span>
            <span class="flex items-center gap-1.5 text-rose-600"><span class="h-3 w-3 rounded-full bg-rose-500" /> Occupied ({{ tableCounts.occupied }})</span>
          </div>
        </div>

        <p v-if="!isLoading && tableList.length === 0" class="text-xs text-gray-400 text-center py-8">
          No tables configured yet.
        </p>
        <div v-else class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-4 gap-3.5">
          <div
            v-for="t in tableList"
            :key="t.num"
            @click="toggleTableStatus(t.num)"
            :class="[
              'cursor-pointer rounded-2xl border-2 p-4 sm:p-5 flex flex-col justify-between h-32 transition shadow-xs select-none active:scale-95',
              t.status === 'Booked'
                ? 'bg-orange-50/70 border-[#f47b20] text-[#f47b20]'
                : t.status === 'Occupied'
                ? 'bg-rose-50/70 border-rose-500 text-rose-700'
                : 'bg-white border-emerald-500/80 text-emerald-800 hover:shadow-md'
            ]"
          >
            <div class="flex justify-between items-center font-bold">
              <span class="text-base font-heading font-black">Table {{ t.num }}</span>
              <span class="text-[10px] px-2 py-0.5 rounded-md bg-white border font-bold shadow-2xs">{{ t.seats }} Seater</span>
            </div>
            <div>
              <span class="text-xs font-black uppercase tracking-wider">{{ t.status }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 4: RESERVATIONS -->
      <div v-if="activeTab === 'Reservations'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-4">
        <div class="flex items-center justify-between border-b border-gray-100 pb-4">
          <h2 class="font-heading text-lg font-black text-gray-900">Table Reservation Register</h2>
          <button class="rounded-xl bg-[#f47b20] px-3.5 py-1.5 text-xs font-bold text-white shadow-xs">
            + New Booking
          </button>
        </div>

        <div class="space-y-3">
          <div
            v-for="res in reservations"
            :key="res.id"
            class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl border border-gray-200/80 bg-gray-50/60 gap-4 text-xs hover:bg-white transition"
          >
            <div>
              <div class="flex items-center gap-2 flex-wrap">
                <span class="font-bold text-gray-900 text-sm">{{ res.name }}</span>
                <span class="text-gray-500 font-mono">({{ res.phone }})</span>
                <span class="rounded-md bg-orange-100 text-[#f47b20] px-2 py-0.5 text-[10px] font-bold">{{ res.id }}</span>
              </div>
              <p class="text-gray-600 mt-1">
                📅 {{ res.date }} • 🕒 {{ res.time }} • 👥 {{ res.guests }} • 🪑 {{ res.area }}
              </p>
            </div>

            <div class="flex items-center gap-2.5">
              <span
                :class="[
                  'px-3 py-1 rounded-full text-xs font-bold',
                  res.status === 'Confirmed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                ]"
              >
                {{ res.status }}
              </span>
              <button class="rounded-lg border border-gray-300 px-3 py-1.5 text-xs font-bold text-gray-700 hover:bg-gray-100 cursor-pointer">
                Assign Seat
              </button>
            </div>
          </div>
          <p v-if="!isLoading && reservations.length === 0" class="text-xs text-gray-400 text-center py-8">
            No table reservations yet.
          </p>
        </div>
      </div>

      <!-- TAB 5: DELIVERY ORDERS -->
      <div v-if="activeTab === 'Delivery Orders'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-4">
        <h2 class="font-heading text-lg font-black text-gray-900 border-b border-gray-100 pb-4">Doorstep Delivery Logistics</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            v-for="del in deliveryList"
            :key="del.id"
            class="rounded-2xl border border-gray-200/90 p-4 space-y-3 bg-gray-50/60 hover:bg-white transition shadow-xs"
          >
            <div class="flex justify-between items-center">
              <span class="font-bold text-gray-900 font-mono">{{ del.id }}</span>
              <span class="rounded-md bg-blue-100 text-blue-700 px-2 py-0.5 text-[10px] font-bold">{{ del.status }}</span>
            </div>
            <p class="text-xs font-bold text-gray-800">{{ del.customer || del.customer_name }}</p>
            <p class="text-xs text-gray-500">📍 {{ del.address || del.delivery_address }}</p>
            <div class="pt-2 border-t border-gray-200 flex justify-between items-center text-xs">
              <span class="text-gray-600 font-medium">🛵 {{ del.driver || 'Rider Assigned' }}</span>
              <span class="text-[#f47b20] font-bold">{{ del.time || del.estimated_time }}</span>
            </div>
          </div>
        </div>
        <p v-if="!isLoading && deliveryList.length === 0" class="text-xs text-gray-400 text-center py-8">
          No active delivery orders.
        </p>
      </div>

      <!-- TAB 6: PARTY BOOKINGS -->
      <div v-if="activeTab === 'Party Bookings'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-4">
        <h2 class="font-heading text-lg font-black text-gray-900 border-b border-gray-100 pb-4">Party & Banquet Requests</h2>
        <div class="space-y-3">
          <div
            v-for="p in parties"
            :key="p.id"
            class="p-4 rounded-xl border border-gray-200/80 bg-orange-50/30 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-xs"
          >
            <div>
              <div class="flex items-center gap-2 flex-wrap">
                <span class="font-bold text-base text-gray-900 font-heading">{{ p.occasion }}</span>
                <span class="rounded-md bg-[#f47b20] text-white px-2 py-0.5 text-[10px] font-bold">{{ p.id }}</span>
              </div>
              <p class="text-gray-700 font-semibold mt-1">Host: {{ p.client }} • Date: {{ p.date }} • Guests: {{ p.guests }}</p>
              <p class="text-gray-500 text-[11px] mt-0.5">Requirements: {{ p.requirements }}</p>
            </div>
            <div class="flex items-center gap-2">
              <a :href="`tel:${p.phone}`" class="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700">
                <Phone :size="14" />
              </a>
              <span class="px-3 py-1 rounded-md bg-emerald-100 text-emerald-700 font-bold text-xs">
                {{ p.status }}
              </span>
            </div>
          </div>
          <p v-if="!isLoading && parties.length === 0" class="text-xs text-gray-400 text-center py-8">
            No party or banquet requests yet.
          </p>
        </div>
      </div>

      <!-- TAB 7: MENU MANAGEMENT -->
      <div v-if="activeTab === 'Menu Management'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-4">
        <div class="flex items-center justify-between border-b border-gray-100 pb-4">
          <h2 class="font-heading text-lg font-black text-gray-900">Food Menu Catalog Editor</h2>
          <button class="rounded-xl bg-[#f47b20] px-3.5 py-1.5 text-xs font-bold text-white shadow-xs">
            + Add New Dish
          </button>
        </div>

        <div class="overflow-x-auto -mx-4 sm:mx-0">
          <table class="w-full text-left text-xs border-collapse min-w-[540px]">
            <thead>
              <tr class="border-b bg-gray-50 text-gray-600 font-bold uppercase text-[11px]">
                <th class="p-3.5">Dish Name</th>
                <th class="p-3.5">Category</th>
                <th class="p-3.5">Price</th>
                <th class="p-3.5">Stock Status</th>
                <th class="p-3.5">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="item in menuItemsList" :key="item.id" class="hover:bg-gray-50">
                <td class="p-3.5 font-bold text-gray-900">{{ item.name }}</td>
                <td class="p-3.5 text-gray-600">{{ item.category }}</td>
                <td class="p-3.5 font-black text-[#f47b20]">₹{{ item.price }}</td>
                <td class="p-3.5">
                  <button
                    @click="handleToggleStock(item.id)"
                    :class="[
                      'px-2.5 py-1 rounded-lg text-[10px] font-bold transition hover:opacity-80 active:scale-95 cursor-pointer',
                      item.status === 'In Stock' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'
                    ]"
                  >
                    {{ item.status }}
                  </button>
                </td>
                <td class="p-3.5 flex items-center gap-2">
                  <button @click="handleToggleStock(item.id)" class="p-1.5 text-gray-600 hover:text-[#f47b20]"><Edit2 :size="14" /></button>
                  <button class="p-1.5 text-gray-600 hover:text-rose-600"><Trash2 :size="14" /></button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-if="!isLoading && menuItemsList.length === 0" class="text-xs text-gray-400 text-center py-8">
            No menu items to display.
          </p>
        </div>
      </div>

      <!-- TAB 8: CUSTOMERS -->
      <div v-if="activeTab === 'Customers'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-4">
        <h2 class="font-heading text-lg font-black text-gray-900 border-b border-gray-100 pb-4">Customer Directory & Loyalty</h2>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div
            v-for="c in customers"
            :key="c.id"
            class="p-4 rounded-2xl border border-gray-200/90 bg-gray-50/60 space-y-2 text-xs hover:bg-white transition"
          >
            <div class="flex justify-between items-center">
              <span class="font-bold text-sm text-gray-900">{{ c.name }}</span>
              <span class="px-2 py-0.5 rounded-md bg-amber-100 text-amber-700 font-bold text-[10px]">{{ c.tag }}</span>
            </div>
            <p class="text-gray-500">📞 {{ c.phone }}</p>
            <div class="pt-2 border-t border-gray-200 flex justify-between text-gray-700 font-semibold">
              <span>Visits: {{ c.visits }}</span>
              <span class="text-[#f47b20] font-black">Total: {{ c.totalSpent }}</span>
            </div>
          </div>
          <p v-if="!isLoading && customers.length === 0" class="text-xs text-gray-400 text-center py-8 col-span-full">
            No customers recorded yet.
          </p>
        </div>
      </div>

      <!-- TAB 9: REPORTS -->
      <div v-if="activeTab === 'Reports'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-100 pb-4">
          <div>
            <h2 class="font-heading text-lg font-black text-gray-900">Analytics & Sales Reports</h2>
            <p class="text-xs text-gray-500">Revenue breakdown, order metrics and category share analytics.</p>
          </div>

          <button
            @click="restroHandler.analytics.downloadCsv()"
            class="flex items-center gap-1.5 rounded-xl bg-[#f47b20] px-4 py-2 text-xs font-bold text-white hover:bg-[#d9630f] transition active:scale-95 shadow-xs shrink-0 cursor-pointer"
          >
            <Download :size="14" /> Export Report (CSV)
          </button>
        </div>

        <div v-if="reportsData" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="p-5 rounded-2xl bg-gray-50 border border-gray-200/90">
            <p class="text-xs font-bold text-gray-500 uppercase">Monthly Revenue</p>
            <p class="text-2xl sm:text-3xl font-black text-gray-900 mt-1 font-heading">{{ reportsData.monthlyRevenue }}</p>
            <p class="text-xs text-emerald-600 font-bold mt-1">{{ reportsData.monthlyGrowth }}</p>
          </div>
          <div class="p-5 rounded-2xl bg-gray-50 border border-gray-200/90">
            <p class="text-xs font-bold text-gray-500 uppercase">Average Order Value</p>
            <p class="text-2xl sm:text-3xl font-black text-gray-900 mt-1 font-heading">{{ reportsData.averageOrderValue }}</p>
            <p class="text-xs text-emerald-600 font-bold mt-1">{{ reportsData.aovGrowth }}</p>
          </div>
          <div class="p-5 rounded-2xl bg-gray-50 border border-gray-200/90">
            <p class="text-xs font-bold text-gray-500 uppercase">Top Selling Category</p>
            <p class="text-2xl sm:text-3xl font-black text-[#f47b20] mt-1 font-heading">{{ reportsData.topCategory }}</p>
            <p class="text-xs text-gray-500 font-medium mt-1">{{ reportsData.topCategoryShare }}</p>
          </div>
        </div>
        <p v-else-if="!isLoading" class="text-xs text-gray-400 text-center py-8">
          No analytics data available yet.
        </p>
      </div>

      <!-- TAB 10: SETTINGS -->
      <div v-if="activeTab === 'Settings'" class="bg-white p-4 sm:p-6 rounded-2xl border border-gray-200/90 shadow-xs space-y-6 max-w-3xl">
        <h2 class="font-heading text-lg font-black text-gray-900 border-b border-gray-100 pb-4">Outlet Settings & Configuration</h2>

        <div class="space-y-4 text-xs">
          <div>
            <label class="font-bold text-gray-700 block mb-1">Outlet Name</label>
            <input
              v-model="outletName"
              type="text"
              class="w-full rounded-xl border border-gray-300 p-3 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>

          <div>
            <label class="font-bold text-gray-700 block mb-1">Default Tax / GST Rate</label>
            <input
              v-model="gstRate"
              type="text"
              class="w-full rounded-xl border border-gray-300 p-3 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>

          <div class="flex items-center justify-between p-3.5 rounded-xl border border-gray-200 bg-gray-50">
            <div>
              <p class="font-bold text-gray-900">Auto-accept Online Delivery Orders</p>
              <p class="text-[11px] text-gray-500">Automatically send incoming online orders directly to kitchen queue</p>
            </div>
            <input
              v-model="autoAccept"
              type="checkbox"
              class="h-5 w-5 accent-[#f47b20] cursor-pointer"
            />
          </div>

          <div class="flex items-center gap-3 pt-2">
            <button
              @click="handleSaveSettings"
              class="rounded-xl bg-[#f47b20] px-6 py-2.5 text-xs font-bold text-white hover:bg-[#d9630f] transition active:scale-95 cursor-pointer shadow-xs"
            >
              Save Settings
            </button>
            <span v-if="settingsSaved" class="text-xs font-bold text-emerald-600 flex items-center gap-1">
              <CheckCircle :size="14" /> Settings saved successfully!
            </span>
            <span v-else-if="settingsError" class="text-xs font-bold text-rose-600 flex items-center gap-1">
              <X :size="14" /> {{ settingsError }}
            </span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
