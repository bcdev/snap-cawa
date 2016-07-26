package org.esa.snap.dataio.nc4;

import org.esa.snap.core.dataio.ProductIO;
import org.esa.snap.core.datamodel.Band;
import org.esa.snap.core.datamodel.Product;
import org.esa.snap.core.datamodel.ProductData;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SnapCawaNc4WriterTest {
    private static SimpleDateFormat COMPACT_ISO_FORMAT = new SimpleDateFormat("yyyyMMdd'T'HHmmss'Z'");

    public static void main(String[] args) throws Exception {
        // todo: extend if needed
//        final Product testproduct = new Product("test", "test", 3, 2);
//        final Band b1Band = testproduct.addBand("cawa_b1_tcwv", ProductData.TYPE_FLOAT32);
//        final Band b1UncertBand = testproduct.addBand("cawa_b2_tcwv_err", ProductData.TYPE_FLOAT32);
//        final Band szaBand = testproduct.addBand("sun_zenith", ProductData.TYPE_FLOAT32);
//
//        // fill with fake data
//        final Band[] bands = testproduct.getBands();
//        for (Band band : bands) {
//            band.setData(new ProductData.Float(new float[]{
//                    1.0F, 3.0F, 7.0F, 5.0F, 6.0F, 13.0F
//            }));
//        }


        final Product testproduct = loadTcwvProduct();
        ProductIO.writeProduct(testproduct, "./BLA_" + testproduct.getName() + ".nc", "NetCDF4-CAWA");
    }

    private static Product loadTcwvProduct() {
        final String tcwvFilename = "subset_TCWV.nc";
        final String tcwvFilePath = SnapCawaNc4WriterTest.class.getResource(tcwvFilename).getPath();

        Product tcwvProduct = null;
        try {
            Logger.getGlobal().log(Level.INFO, "Reading TCWV file '" + tcwvFilePath + "'...");
            tcwvProduct = ProductIO.readProduct(new File(tcwvFilePath));
        } catch (IOException e) {
            Logger.getGlobal().log(Level.WARNING, "Warning: cannot open or read AOT climatology file.");
        }
        return tcwvProduct;
    }
}
