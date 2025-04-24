'use client'

import { useScroll } from '../hooks/useScroll';


export default function Header() {
    const scroll = useScroll();

    return (
        <header className={`sticky top-0 z-50 ${scroll > 0 ? 'bg-midnight/90 shadow-md backdrop-blur-sm' : 'bg-midnight hover:bg-midnight/90 hover:shadow-md hover:backdrop-blur-sm'} transition-shadow duration-300 ease-in-out`}>
            <nav className="px-8 py-4 flex gap-4 items-center">
                <a href="/" className="flex items-center gap-2">
                    <img
                        src="/icon.svg"
                        alt="b01lerchain logo"
                        className="size-6"
                    />
                    <h3 className="font-semibold">b01lerchain</h3>
                </a>

                <a href="/#" className="ml-auto text-inherit hover:no-underline">
                    About
                </a>
                <a href="/#" className="text-inherit hover:no-underline">
                    FAQ
                </a>
                <a href="/flag" className="text-inherit hover:no-underline">
                    Flag
                </a>
            </nav>
        </header>
    )
}
