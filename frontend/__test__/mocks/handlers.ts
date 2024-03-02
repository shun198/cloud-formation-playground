import { AuthInfoHandlers } from "./authInfo";
import { CustomerListHandlers } from "./customer";

const handlers = [...AuthInfoHandlers, ...CustomerListHandlers];

export default handlers;
