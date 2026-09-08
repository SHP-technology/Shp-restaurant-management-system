import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ShoppingBag, Search, Plus, Check, Star, ArrowLeft, Filter } from 'lucide-react'

interface MenuItem {
  id: number
  name: string
  price: number
  category: string
  description: string
  rating: number
  prepTime: string
  isVeg: boolean
  isSpecial?: boolean
  image: string
}

const menuItems: MenuItem[] = [
  {
    id: 1,
    name: 'Truffle Mushroom Pizza',
    price: 349,
    category: 'Pizza',
    description: 'Wild forest mushrooms, black truffle oil, fresh mozzarella, and aromatic basil.',
    rating: 4.9,
    prepTime: '20 mins',
    isVeg: true,
    isSpecial: true,
    image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 2,
    name: 'Artisan Smash Burger',
    price: 279,
    category: 'Burgers',
    description: 'Double smashed patty, aged cheddar, caramelised onions, brioche bun, signature sauce.',
    rating: 4.8,
    prepTime: '15 mins',
    isVeg: false,
    isSpecial: true,
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 3,
    name: 'Spicy Schezwan Noodles',
    price: 249,
    category: 'Asian',
    description: 'Wok-tossed hand-pulled noodles with crisp vegetables and chili schezwan glaze.',
    rating: 4.7,
    prepTime: '18 mins',
    isVeg: true,
    image: 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 4,
    name: 'Burrata Margherita Pizza',
    price: 389,
    category: 'Pizza',
    description: 'Creamy San Marzano tomato sauce, fresh creamy burrata ball, micro basil.',
    rating: 4.9,
    prepTime: '22 mins',
    isVeg: true,
    image: 'https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 5,
    name: 'Dum Pukht Veg Biryani',
    price: 299,
    category: 'Indian',
    description: 'Aromatic long-grain basmati, saffron, seasonal vegetables sealed in clay pot.',
    rating: 4.8,
    prepTime: '25 mins',
    isVeg: true,
    image: 'https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 6,
    name: 'Matcha Citrus Sparkler',
    price: 169,
    category: 'Beverages',
    description: 'Ceremonial matcha whisked with fresh Yuzu juice, mint, and sparkling soda.',
    rating: 4.6,
    prepTime: '5 mins',
    isVeg: true,
    image: 'https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 7,
    name: 'Molten Belgian Chocolate Lava',
    price: 219,
    category: 'Desserts',
    description: 'Warm dark chocolate cake with a oozing center, served with vanilla bean ice cream.',
    rating: 4.9,
    prepTime: '12 mins',
    isVeg: true,
    image: 'https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=600&q=80',
  },
]

const categories = ['All', 'Pizza', 'Burgers', 'Asian', 'Indian', 'Beverages', 'Desserts']

export function MenuPage() {
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [searchQuery, setSearchQuery] = useState('')
  const [vegOnlyFilter, setVegOnlyFilter] = useState(false)
  const [cart, setCart] = useState<{ [key: number]: number }>({})

  const filteredItems = menuItems.filter((item) => {
    const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesVeg = !vegOnlyFilter || item.isVeg
    return matchesCategory && matchesSearch && matchesVeg
  })

  const addToCart = (id: number) => {
    setCart((prev) => ({ ...prev, [id]: (prev[id] || 0) + 1 }))
  }

  const totalCartCount = Object.values(cart).reduce((a, b) => a + b, 0)
  const totalCartPrice = Object.entries(cart).reduce((sum, [id, count]) => {
    const item = menuItems.find((m) => m.id === Number(id))
    return sum + (item ? item.price * count : 0)
  }, 0)

  return (
    <div className="min-h-screen bg-[#fffdf9] text-[#1d211e]">
      {/* Top Header */}
      <header className="sticky top-0 z-40 border-b border-gray-200 bg-white px-4 sm:px-6 py-3.5 shadow-sm">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Link to="/" className="flex items-center gap-1.5 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
              <ArrowLeft size={16} /> Home
            </Link>
            <span className="h-4 w-px bg-gray-200" />
            <h1 className="font-heading text-lg sm:text-xl font-bold text-gray-900">Gourmet Menu</h1>
          </div>

          <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
            <div className="relative flex-1 sm:flex-none">
              <Search className="absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search menu..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full sm:w-56 rounded-full border border-gray-300 bg-gray-50 pl-8 pr-3 py-1.5 text-xs text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none"
              />
            </div>

            <button className="relative flex items-center gap-1.5 rounded-full bg-[#f47b20] px-3.5 py-1.5 sm:px-4 sm:py-2 text-xs font-bold text-white transition hover:bg-[#d9630f] shrink-0">
              <ShoppingBag size={14} />
              <span>Cart</span>
              {totalCartCount > 0 && (
                <span className="ml-0.5 rounded-full bg-white px-1.5 py-0.5 text-[9px] text-[#f47b20] font-bold">
                  {totalCartCount}
                </span>
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 py-6 sm:py-8">
        {/* Category Pills & Filters */}
        <div className="mb-6 sm:mb-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex w-full sm:w-auto overflow-x-auto pb-2 sm:pb-0 gap-2 scrollbar-none">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`rounded-full px-4 py-1.5 sm:px-5 sm:py-2 text-xs font-bold transition shrink-0 ${
                  selectedCategory === cat
                    ? 'bg-[#f47b20] text-white shadow-sm'
                    : 'border border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          <button
            onClick={() => setVegOnlyFilter(!vegOnlyFilter)}
            className={`flex items-center gap-1.5 rounded-full border px-3.5 py-1.5 text-xs font-bold transition self-end sm:self-auto shrink-0 ${
              vegOnlyFilter
                ? 'border-emerald-600 bg-emerald-50 text-emerald-700'
                : 'border-gray-200 bg-white text-gray-600 hover:text-gray-900'
            }`}
          >
            <Filter size={13} />
            <span>Pure Veg</span>
            {vegOnlyFilter && <Check size={13} className="text-emerald-600" />}
          </button>
        </div>

        {/* Menu Items Grid */}
        <div className="grid gap-4 sm:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {filteredItems.map((item) => (
            <div
              key={item.id}
              className="group flex flex-col justify-between overflow-hidden rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition hover:shadow-md hover:border-orange-300"
            >
              <div>
                <div className="relative mb-3.5 h-44 sm:h-48 overflow-hidden rounded-lg">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                  {item.isSpecial && (
                    <span className="absolute left-3 top-3 rounded-md bg-[#f47b20] px-2.5 py-1 text-[10px] font-bold text-white shadow-sm">
                      Chef's Special
                    </span>
                  )}
                  <span
                    className={`absolute right-3 top-3 rounded-md border px-2 py-0.5 text-[10px] font-bold bg-white/90 backdrop-blur-sm ${
                      item.isVeg
                        ? 'border-emerald-600 text-emerald-700'
                        : 'border-rose-600 text-rose-700'
                    }`}
                  >
                    {item.isVeg ? '● VEG' : '▲ NON-VEG'}
                  </span>
                </div>

                <div className="flex items-start justify-between gap-2">
                  <h3 className="font-heading text-base sm:text-lg font-bold text-gray-900 group-hover:text-[#f47b20] transition">
                    {item.name}
                  </h3>
                  <div className="flex items-center gap-1 rounded bg-amber-50 px-2 py-0.5 text-[11px] font-bold text-amber-700 border border-amber-200 shrink-0">
                    <Star size={11} className="fill-amber-500 text-amber-500" />
                    {item.rating}
                  </div>
                </div>

                <p className="mt-1.5 text-xs leading-relaxed text-gray-500">
                  {item.description}
                </p>
              </div>

              <div className="mt-5 flex items-center justify-between border-t border-gray-100 pt-3.5">
                <div>
                  <span className="text-[10px] text-gray-400 font-medium">Price</span>
                  <p className="text-lg sm:text-xl font-bold text-gray-900">₹{item.price}</p>
                </div>

                <button
                  onClick={() => addToCart(item.id)}
                  className="flex items-center gap-1.5 rounded-md bg-[#f47b20] px-3.5 py-2 text-xs font-bold text-white transition hover:bg-[#d9630f]"
                >
                  <Plus size={14} />
                  <span>ADD {cart[item.id] ? `(${cart[item.id]})` : ''}</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Floating Cart Bar */}
      {totalCartCount > 0 && (
        <div className="fixed bottom-4 left-1/2 z-50 flex w-[calc(100%-32px)] max-w-md -translate-x-1/2 items-center justify-between rounded-full bg-[#1d211e] px-5 py-3 shadow-2xl text-white">
          <div>
            <p className="text-[10px] text-gray-400">{totalCartCount} items selected</p>
            <p className="text-sm sm:text-base font-bold text-[#f4a13d]">Total: ₹{totalCartPrice}</p>
          </div>
          <Link
            to="/delivery"
            className="flex items-center gap-1.5 rounded-full bg-[#f47b20] px-4 py-1.5 text-xs font-bold text-white transition hover:bg-[#d9630f]"
          >
            Checkout <ArrowLeft size={13} className="rotate-180" />
          </Link>
        </div>
      )}
    </div>
  )
}
