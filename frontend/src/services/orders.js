import { request } from './api';
import { getStoredOrders, setStoredOrders, getStoredProducts } from './mockData';

export const orderService = {
  // Create Order Request (Buyer Flow)
  async createOrderRequest(orderData) {
    try {
      return await request('/api/orders/request', {
        method: 'POST',
        body: JSON.stringify(orderData)
      });
    } catch (e) {
      console.warn("Backend unavailable, saving order locally", e);
      const orders = getStoredOrders();
      const products = getStoredProducts();
      const product = products.find(p => p.id === orderData.product_id) || {};

      const newOrder = {
        id: `ord-${Date.now().toString(16).slice(-6)}`,
        product_id: orderData.product_id,
        product_title: product.title || 'Artisan Handcraft',
        artisan_id: product.artisan_id || 'art-001',
        buyer_name: orderData.buyer_name,
        buyer_contact: orderData.buyer_contact,
        quantity: Number(orderData.quantity) || 1,
        notes: orderData.notes || '',
        price_offered: Number(orderData.price_offered) || product.suggested_price_min || 750,
        status: 'pending',
        created_at: new Date().toISOString()
      };

      orders.unshift(newOrder);
      setStoredOrders(orders);
      return newOrder;
    }
  },

  // List Orders (filtered by product_id or artisan_id)
  async listOrders({ product_id, artisan_id } = {}) {
    const params = new URLSearchParams();
    if (product_id) params.append('product_id', product_id);
    if (artisan_id) params.append('artisan_id', artisan_id);

    try {
      return await request(`/api/orders?${params.toString()}`);
    } catch (e) {
      console.warn("Backend unavailable, reading local orders", e);
      let orders = getStoredOrders();
      if (product_id) {
        orders = orders.filter(o => o.product_id === product_id);
      }
      if (artisan_id) {
        orders = orders.filter(o => !o.artisan_id || o.artisan_id === artisan_id);
      }
      return orders;
    }
  },

  // Update order status (accept/fulfill)
  async updateOrderStatus(orderId, status) {
    const orders = getStoredOrders();
    const index = orders.findIndex(o => o.id === orderId);
    if (index !== -1) {
      orders[index].status = status;
      setStoredOrders(orders);
      return orders[index];
    }
    return null;
  }
};
