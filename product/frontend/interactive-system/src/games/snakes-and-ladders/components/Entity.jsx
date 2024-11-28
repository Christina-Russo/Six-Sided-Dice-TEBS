import React from 'react';
import '../styles/game-styles.css';

/**
 * Renders entities (ie. snakes and ladders) on the grid.
 * Dynamically scales entities to stretch across the start and end positons.
 * 
 * @param {string} type - name of entity, currently either "snake" or "ladder"
 * @param {[number, number]} start - coordinates of start position on grid
 * @param {[number, number]} end - coordinates of end position on grid
 */
export default function Entity({type, start, end}) {
    
    //units for deltas and distance are no. grid squares
    const dr = end[0] - start[0]; //row delta
    const dc = end[1] - start[1]; //col delta
    const dist = Math.sqrt(dr*dr + dc*dc); //distance in no. grid squares
    const angle = Math.atan2(dr, dc)

    const squareSize = 2.43; //square side + border in cm
    const squareOffset = 0.8; //helps position entities in the middle of square

    //determines whether to render a snake or a ladder
    function createBody() {
        if (type === "ladder") {
            return <Ladder dist={dist}/>
        } else if (type === "snake") {
            return <Snake/>
        } else {
            console.log("Error: unknown entity type")
            return <></>
        }
    }

    function getHeight() {
        if (type === "ladder") {
            return "1.5cm"
        } else {
            return `${0.42*(1 + dist*0.21)}cm`
        }
    }

    return (
    <div className={type}>
        <div className="entity-body" style ={{
            width: `${dist*squareSize}cm`,
            height: getHeight(),
            transformOrigin: "left",
            transform: `rotate(${angle}rad)`,
            top: `${start[0]*squareSize + squareOffset}cm`,
            left: `${start[1]*squareSize + squareOffset + 0.5}cm`
        }}>
            {createBody()}
        </div>
    </div>
    );
}

/**
 * Renders the body segments of a ladder
 * @param {number} dist - length of the ladder in no. squares
 */
function Ladder({ dist }) {
    //for functionally mapping LadderSegment components
    const segments = Array(Math.ceil(dist)).fill(null);

    return <>{segments.map((e, i) => (<LadderSegment key={i}/>))}</>
}

/**
 * Renders a ladder body segment
 */
function LadderSegment() {
    return (
        <div className='ladder-bbox'>
            <div className='ladder-side'></div>
            <div className='ladder-rung'></div>
            <div className='ladder-side'></div>
        </div>
    )
}

/**
 * Renders the head, body, and tail of a snake
 */
function Snake() {
    return (
        <>
        <div className="snake-head">
            <SnakeHead/>
        </div>
        <div className='snake-body'></div>
        <div className='snake-tail'>
            <SnakeTail/>
        </div>
        </>
    )
}

/**
 * SVG for a snake's head
 */
function SnakeHead() {
    return (
    <svg xmlns="http://www.w3.org/2000/svg" 
        width="2cm"
        viewBox="0 0 60 60">
    <defs/>
    <path id="shape0" transform="matrix(2.23170721069056 0 0 0.247457592475898 30.5538991166098 45.5877969429269)" fill="none" stroke="#c03435" strokeWidth="9.6" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L3.55271e-15 61.0266" sodipodi:nodetypes="cc"/><path id="shape1" transform="matrix(0.981884028181669 0 0 0.836842111681633 30.3234773859036 16.1238938919068)" fill="none" stroke="#e7a08c" strokeWidth="3.5136" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L0 11.1606" sodipodi:nodetypes="cc"/><path id="shape2" transform="matrix(0.981884028181669 0 0 0.836842111681633 24.3732598668843 10.5505255011908)" fill="none" stroke="#e7a08c" strokeWidth="3.5136" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M6.06 6.84L0 0" sodipodi:nodetypes="cc"/><path id="shape3" transform="matrix(0.981884028181669 0 0 0.836842111681633 30.3234773859036 10.2492623449359)" fill="none" stroke="#e7a08c" strokeWidth="3.5136" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 6.84L5.28 0" sodipodi:nodetypes="cc"/><ellipse id="shape4" transform="matrix(0.834259305320345 0 0 0.834259305320345 17.0844439901371 22.8375542010618)" rx="16.2" ry="20.52" cx="16.2" cy="20.52" fill="none" stroke="#c03435" strokeWidth="9.2808" strokeLinecap="square" strokeLinejoin="bevel"/><ellipse id="shape5" transform="matrix(1.18333337344367 0 0 1.47321429492418 25.4800009285716 31.9714317415475)" rx="4.2" ry="5.28" cx="4.2" cy="5.28" fill="none" stroke="#c03435" strokeWidth="9.2808" strokeLinecap="square" strokeLinejoin="bevel"/><circle id="shape6" transform="matrix(0.804166671490032 0.000111989459565278 -0.000111989459565278 0.804166671490032 21.1641813533027 35.4126360236508)" r="1.68" cx="1.68" cy="1.68" fill="none" stroke="#000000" strokeWidth="3.5136" strokeLinecap="square" strokeLinejoin="bevel"/><circle id="shape7" transform="matrix(0.804166671490032 0.000111989459565278 -0.000111989459565278 0.804166671490032 37.9641811903951 35.4149756168834)" r="1.68" cx="1.68" cy="1.68" fill="none" stroke="#000000" strokeWidth="3.5136" strokeLinecap="square" strokeLinejoin="bevel"/>
    </svg>
    )
}

/**
 * SVG for a snake's tail
 */
function SnakeTail() {
    return (
    <svg xmlns="http://www.w3.org/2000/svg" 
        width="2cm"
        viewBox="0 0 60 60">
    <defs/>
    <path id="shape0" transform="matrix(2.23170721069056 0 0 0.121186434125192 30.5538992337184 -4.21830509455577)" fill="none" stroke="#c03435" strokeWidth="9.6" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L3.55271e-15 61.0266" sodipodi:nodetypes="cc"/><path id="shape1" transform="matrix(0.937499939405592 0 0 1 20.8124971945848 3.59999979493061)" fill="none" stroke="#c03435" strokeWidth="1.7616" strokeLinecap="square" strokeLinejoin="bevel" d="M0 0L21.06 0.18L10.2 46.44L0 0" sodipodi:nodetypes="cccc"/><path id="shape2" transform="translate(30, 3.05999977748395)" fill="none" stroke="#c03435" strokeWidth="1.572" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 42.12L0 0" sodipodi:nodetypes="cc"/><path id="shape3" transform="translate(30, 2.69999980366231)" fill="none" stroke="#c03435" strokeWidth="1.572" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 41.58L6 0" sodipodi:nodetypes="cc"/><path id="shape4" transform="translate(30, 4.31999968585969)" fill="none" stroke="#c03435" strokeWidth="1.572" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 40.14L8.52 0" sodipodi:nodetypes="cc"/><path id="shape5" transform="translate(30, 3.95999971203805)" fill="none" stroke="#c03435" strokeWidth="1.572" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 41.58L9.6 0" sodipodi:nodetypes="cc"/><path id="shape6" transform="translate(21.9599984031201, 0)" fill="none" stroke="#c03435" strokeWidth="1.572" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M8.04 41.94L0 0" sodipodi:nodetypes="cc"/><path id="shape7" transform="translate(21.9599984031201, 2.69999980366231)" fill="none" stroke="#c03435" strokeWidth="1.572" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L8.04 32.4" sodipodi:nodetypes="cc"/><path id="shape8" transform="translate(21.9599984031201, 6.29999954187872)" fill="none" stroke="#c03435" strokeWidth="1.572" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L8.04 28.08" sodipodi:nodetypes="cc"/><path id="shape9" transform="translate(23.5799982853175, 13.6799990052224)" fill="none" stroke="#c03435" strokeWidth="1.572" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L6.42 21.78" sodipodi:nodetypes="cc"/><path id="shape10" transform="translate(30, 3.77999972512723)" fill="none" stroke="#c03435" strokeWidth="3.8328" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M7.44 0L0 34.92" sodipodi:nodetypes="cc"/><path id="shape11" transform="translate(23.3999982984067, 2.69999980366231)" fill="none" stroke="#c03435" strokeWidth="3.8328" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L8.46 33.48" sodipodi:nodetypes="cc"/><path id="shape12" transform="translate(30, 3.23999976439477)" fill="none" stroke="#c03435" strokeWidth="3.8328" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M4.38 0L0 26.76" sodipodi:nodetypes="cc"/><path id="shape13" transform="translate(25.3799981544257, 2.33999982984067)" fill="none" stroke="#c03435" strokeWidth="3.8328" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L4.62 21.78" sodipodi:nodetypes="cc"/><path id="shape14" transform="translate(28.079997958088, 3.05999977748395)" fill="none" stroke="#c03435" strokeWidth="3.8328" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M0 0L1.92 19.44" sodipodi:nodetypes="cc"/><path id="shape15" transform="translate(30, 1.97999985601903)" fill="none" stroke="#c03435" strokeWidth="3.8328" strokeLinecap="square" strokeLinejoin="miter" strokeMiterlimit="2" d="M1.86 0L0 34.92" sodipodi:nodetypes="cc"/>
    </svg>
    )
}