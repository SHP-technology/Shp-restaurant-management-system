import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { MenuItemData } from '../services/api'

export interface CartItem {
  item: MenuItemData
  quantity: number
}

const STORAGE_KEY = 'shp_restro_cart'

function loadSavedCart(): CartItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed)) {
        return parsed
      }
    }
  } catch {
    // Ignore error
  }
  return []
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>(loadSavedCart())
  const couponCode = ref('')
  const couponDiscount = ref(0)
  const deliveryAddress = ref('')
  const customerName = ref('')
  const customerPhone = ref('')
  const deliveryInstructions = ref('')
  const paymentMethod = ref<'cod' | 'upi' | 'card'>('upi')

  function saveToStorage() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value))
    } catch {
      // Ignore error
    }
  }

  function getItemQuantity(id: number | string): number {
    const found = items.value.find((i) => String(i.item.id) === String(id))
    return found ? found.quantity : 0
  }

  function addItem(dish: MenuItemData) {
    const existing = items.value.find((i) => String(i.item.id) === String(dish.id))
    if (existing) {
      existing.quantity += 1
    } else {
      items.value.push({
        item: { ...dish },
        quantity: 1,
      })
    }
    saveToStorage()
  }

  function decrementItem(id: number | string) {
    const idx = items.value.findIndex((i) => String(i.item.id) === String(id))
    if (idx !== -1) {
      if (items.value[idx].quantity <= 1) {
        items.value.splice(idx, 1)
      } else {
        items.value[idx].quantity -= 1
      }
      saveToStorage()
    }
  }

  function updateQuantity(id: number | string, qty: number) {
    const idx = items.value.findIndex((i) => String(i.item.id) === String(id))
    if (idx !== -1) {
      if (qty <= 0) {
        items.value.splice(idx, 1)
      } else {
        items.value[idx].quantity = qty
      }
      saveToStorage()
    }
  }

  function removeItem(id: number | string) {
    const idx = items.value.findIndex((i) => String(i.item.id) === String(id))
    if (idx !== -1) {
      items.value.splice(idx, 1)
      saveToStorage()
    }
  }

  function clearCart() {
    items.value = []
    couponCode.value = ''
    couponDiscount.value = 0
    saveToStorage()
  }

  function applyCoupon(code: string): { success: boolean; message: string } {
    const cleanCode = code.trim().toUpperCase()
    if (!cleanCode) {
      couponCode.value = ''
      couponDiscount.value = 0
      return { success: false, message: 'Please enter a valid coupon code.' }
    }

    if (cleanCode === 'SHP20') {
      couponCode.value = cleanCode
      couponDiscount.value = Math.round(subtotal.value * 0.2)
      return { success: true, message: '20% OFF applied successfully!' }
    } else if (cleanCode === 'WELCOME15') {
      couponCode.value = cleanCode
      couponDiscount.value = Math.round(subtotal.value * 0.15)
      return { success: true, message: '15% Welcome discount applied!' }
    } else if (cleanCode === 'FEAST50') {
      couponCode.value = cleanCode
      couponDiscount.value = 50
      return { success: true, message: 'Flat ₹50 OFF applied!' }
    } else {
      // Default sample promo
      couponCode.value = cleanCode
      couponDiscount.value = 30
      return { success: true, message: `Coupon "${cleanCode}" applied: ₹30 saved!` }
    }
  }

  function removeCoupon() {
    couponCode.value = ''
    couponDiscount.value = 0
  }

  const totalCount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const subtotal = computed(() => {
    return items.value.reduce((sum, item) => sum + Number(item.item.price) * item.quantity, 0)
  })

  const gstAmount = computed(() => {
    return Math.round(subtotal.value * 0.05)
  })

  const grandTotal = computed(() => {
    return Math.max(0, subtotal.value + gstAmount.value - couponDiscount.value)
  })

  return {
    items,
    couponCode,
    couponDiscount,
    deliveryAddress,
    customerName,
    customerPhone,
    deliveryInstructions,
    paymentMethod,
    totalCount,
    subtotal,
    gstAmount,
    grandTotal,
    getItemQuantity,
    addItem,
    decrementItem,
    updateQuantity,
    removeItem,
    clearCart,
    applyCoupon,
    removeCoupon,
  }
})
