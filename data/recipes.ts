
export interface Recipe {
    id: string
    title: string
    description: string
    imageUrl: string
    ingredients: string[]
    steps: string[]
  }
  
  export const recipes: Recipe[] = [
    {
      id: 'r1',
      title: 'Machaca con Huevo',
      description: 'Clásica receta norteña que combina machaca con huevos revueltos',
      imageUrl: '/images/receta-machaca-huevo.jpg',
      ingredients: [
        '2 huevos',
        '100g Machaca Premium',
        '1/2 cebolla picada',
        'Sal y pimienta al gusto',
        'Aceite de oliva'
      ],
      steps: [
        'Calienta aceite en un sartén',
        'Agrega la cebolla y sofríe hasta transparente',
        'Añade la machaca y cocina por 2 minutos',
        'Bate los huevos con sal y pimienta y agrégalos al sartén',
        'Revuelve hasta que los huevos estén cocidos',
        'Sirve caliente'
      ]
    },
    {
      id: 'r2',
      title: 'Machaca con Verdura',
      description: 'Una versión saludable con verduras frescas y machaca',
      imageUrl: '/images/receta-machaca-verdura.jpg',
      ingredients: [
        '100g Machaca Premium',
        '1/2 cebolla en rodajas',
        '1 tomate picado',
        '1 pimiento verde en tiras',
        'Sal al gusto',
        'Aceite'
      ],
      steps: [
        'Calienta aceite y sofríe la cebolla',
        'Agrega el pimiento y el tomate y cocina 3 minutos',
        'Incorpora la machaca y mezcla bien',
        'Sazona con sal y cocina 2 minutos más',
        'Sirve acompañado de tortillas'
      ]
    },
    {
      id: 'r3',
      title: 'Machaca con Papa',
      description: 'Deliciosas papas guisadas con machaca para un desayuno completo',
      imageUrl: '/images/receta-machaca-papa.jpg',
      ingredients: [
        '100g Machaca Premium',
        '2 papas medianas peladas y en cubos',
        '1/2 cebolla picada',
        'Aceite',
        'Sal y pimienta'
      ],
      steps: [
        'Hierve las papas hasta que estén tiernas y escurre',
        'En un sartén con aceite, sofríe la cebolla hasta dorar',
        'Añade las papas y la machaca, mezcla bien',
        'Sazona con sal y pimienta',
        'Cocina 5 minutos más y sirve'
      ]
    }
  ]
  