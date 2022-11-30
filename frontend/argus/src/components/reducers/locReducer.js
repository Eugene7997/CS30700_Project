export const locReducer = (state, action) => {
    switch(action.type) {
        case "ADD_LOC":
            return [...state, {
                x: action.x,
                y: action.y,
                ea: action.ea
            }]
        case "REMOVE_LOC":
            return state.filter(action.ea)
        default:
            return state
    }
}