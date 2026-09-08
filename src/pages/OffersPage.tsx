import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Percent, Gift, Copy, Check } from 'lucide-react'

export function OffersPage() {
  const [copiedCode, setCopiedCode] = useState<string | null>(null)

  const offers = [
    {
      title: 'Weekend Special Offer',
      discount: 'Flat 20% OFF',
      minSpend: 'On all orders above ₹499',
      code: 'SHP20',
      tag: 'HOT DEAL',
      badgeColor: 'bg-rose-500 text-white',
    },
    {
      title: 'Welcome First Order',
      discount: '15% OFF',
      minSpend: 'On your very first order',
      code: 'WELCOME15',
      tag: 'NEW USER',
      badgeColor: 'bg-[#f47b20] text-white',
    },
    {
      title: 'Sweet Delight',
      discount: 'Free Dessert',
      minSpend: 'On orders above ₹699',
      code: 'DESSERT',
      tag: 'SPECIAL',
      badgeColor: 'bg-emerald-600 text-white',
    },
  ]

  const handleCopy = (code: string) => {
    navigator.clipboard.writeText(code)
    setCopiedCode(code)
    setTimeout(() => setCopiedCode(null), 2000)
  }

  return (
    <div className="min-h-screen bg-[#fffdf9] text-[#1d211e]">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white px-6 py-4 shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
            <ArrowLeft size={16} /> Home
          </Link>
          <span className="font-heading text-lg font-bold text-gray-900">Offers & Discounts</span>
          <div className="w-16" />
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-12">
        <div className="mb-10 text-center">
          <span className="inline-flex items-center gap-2 rounded-full bg-orange-100 px-4 py-1.5 text-xs font-bold text-[#f47b20]">
            <Percent size={14} /> Exclusive Deals
          </span>
          <h1 className="mt-3 font-heading text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Save Big on Gourmet Meals
          </h1>
          <p className="mt-2 text-xs sm:text-sm text-gray-500">
            Apply discount codes at checkout for instant savings on dine-in & doorstep delivery.
          </p>
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {offers.map((offer) => (
            <div
              key={offer.code}
              className="relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition hover:shadow-md"
            >
              <span className={`absolute top-4 right-4 rounded-full px-3 py-1 text-[10px] font-bold ${offer.badgeColor}`}>
                {offer.tag}
              </span>

              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-orange-50 text-[#f47b20]">
                <Gift size={24} />
              </div>

              <h3 className="font-heading text-lg font-bold text-gray-900">{offer.title}</h3>
              <p className="text-2xl font-black text-[#f47b20] mt-1">{offer.discount}</p>
              <p className="text-xs text-gray-500 mt-1">{offer.minSpend}</p>

              <div className="mt-6 flex items-center justify-between border-t border-dashed border-gray-200 pt-4">
                <span className="font-mono text-xs font-bold tracking-wider text-gray-800 bg-gray-100 px-3 py-1.5 rounded border border-gray-300">
                  {offer.code}
                </span>

                <button
                  onClick={() => handleCopy(offer.code)}
                  className="flex items-center gap-1.5 rounded-md bg-[#f47b20] px-3.5 py-1.5 text-xs font-bold text-white transition hover:bg-[#d9630f]"
                >
                  {copiedCode === offer.code ? (
                    <>
                      <Check size={14} /> Copied
                    </>
                  ) : (
                    <>
                      <Copy size={14} /> Copy Code
                    </>
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
