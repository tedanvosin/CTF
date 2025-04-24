import type { ReactNode } from 'react';


type AdCardProps = {
    title: string,
    src: string,
    children: ReactNode,
}
export default function AdCard(props: AdCardProps) {
    return (
        <div className="bg-midnight border border-white/10 rounded-2xl shadow-xl max-w-sm overflow-hidden">
            <img
                src={props.src}
                alt="person"
                className="w-full mb-4 h-44 object-cover object-center"
            />
            <h2 className="text-xl font-bold mb-3 px-7">
                {props.title}
            </h2>
            <p className="text-sm px-7 pb-6 text-primary">
                {props.children}
            </p>
        </div>
    )
}
