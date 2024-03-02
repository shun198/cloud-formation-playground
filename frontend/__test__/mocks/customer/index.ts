import { HttpResponse, PathParams, http } from "msw";
import { CustomerType } from "@/components/forms/type";
import { MockCustomerListData } from "./response";

export const CustomerListHandlers = [
  http.get<PathParams, CustomerType>(`localhost/back/api/customers`, () => {
    return HttpResponse.json(MockCustomerListData);
  }),
];
